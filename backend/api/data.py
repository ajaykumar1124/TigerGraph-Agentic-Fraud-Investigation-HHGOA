"""Data Upload API - Upload real transaction data for fraud investigation"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any
import pandas as pd
import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/data/upload")
async def upload_data(
    file: UploadFile = File(...),
    data_type: str = Form("transactions")
) -> Dict[str, Any]:
    """
    Upload banking transaction data (CSV or JSON)
    
    - **file**: CSV or JSON file with transaction data
    - **data_type**: Type of data (transactions, users, cards)
    
    Required CSV columns: transaction_id, user_id, amount
    Optional: card_id, merchant_id, device_id, ip_address, timestamp, status
    """
    try:
        logger.info(f"Receiving upload: {file.filename}")
        
        # Read file content
        content = await file.read()
        
        # Determine file type and parse
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        elif file.filename.endswith('.json'):
            df = pd.read_json(io.StringIO(content.decode('utf-8')))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Use CSV, JSON, or Excel (xlsx)"
            )
        
        logger.info(f"Parsed {len(df)} records from {file.filename}")
        
        # Validate required columns
        required = ['transaction_id', 'user_id', 'amount']
        missing = [col for col in required if col not in df.columns]
        
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {missing}. Required: {required}"
            )
        
        # Calculate statistics
        stats = {
            'records': len(df),
            'unique_users': df['user_id'].nunique(),
            'unique_transactions': df['transaction_id'].nunique(),
            'unique_cards': df['card_id'].nunique() if 'card_id' in df.columns else 0,
            'unique_merchants': df['merchant_id'].nunique() if 'merchant_id' in df.columns else 0,
            'total_amount': float(df['amount'].sum()) if 'amount' in df.columns else 0,
            'avg_amount': float(df['amount'].mean()) if 'amount' in df.columns else 0
        }
        
        # Save uploaded data
        output_dir = Path('backend/memory/uploaded_data')
        output_dir.mkdir(exist_ok=True, parents=True)
        output_file = output_dir / f"{file.filename}"
        df.to_csv(output_file, index=False)
        
        logger.info(f"✓ Saved to {output_file}")
        logger.info(f"✓ Statistics: {stats}")
        
        return {
            "status": "success",
            "message": f"Successfully uploaded {len(df)} records",
            "filename": file.filename,
            "saved_to": str(output_file),
            "statistics": stats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@router.get("/data/stats")
async def get_data_stats() -> Dict[str, Any]:
    """Get statistics about uploaded data"""
    try:
        upload_dir = Path('backend/memory/uploaded_data')
        
        if not upload_dir.exists():
            return {
                "status": "no_data",
                "message": "No data uploaded yet",
                "files": 0
            }
        
        # Count files
        csv_files = list(upload_dir.glob('*.csv'))
        
        # Load and aggregate stats
        total_records = 0
        total_users = set()
        total_transactions = set()
        
        for file in csv_files:
            try:
                df = pd.read_csv(file)
                total_records += len(df)
                if 'user_id' in df.columns:
                    total_users.update(df['user_id'].unique())
                if 'transaction_id' in df.columns:
                    total_transactions.update(df['transaction_id'].unique())
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")
        
        return {
            "status": "ok",
            "files_uploaded": len(csv_files),
            "total_records": total_records,
            "unique_users": len(total_users),
            "unique_transactions": len(total_transactions),
            "upload_directory": str(upload_dir)
        }
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


@router.get("/data/files")
async def list_uploaded_files() -> Dict[str, Any]:
    """List all uploaded data files"""
    try:
        upload_dir = Path('backend/memory/uploaded_data')
        
        if not upload_dir.exists():
            return {"files": []}
        
        files = []
        for file in upload_dir.glob('*'):
            if file.is_file():
                files.append({
                    "filename": file.name,
                    "size_bytes": file.stat().st_size,
                    "modified": file.stat().st_mtime
                })
        
        return {
            "status": "ok",
            "count": len(files),
            "files": files
        }
        
    except Exception as e:
        logger.error(f"List files error: {e}")
        raise HTTPException(500, str(e))


@router.delete("/data/files/{filename}")
async def delete_uploaded_file(filename: str) -> Dict[str, Any]:
    """Delete an uploaded data file"""
    try:
        file_path = Path('backend/memory/uploaded_data') / filename
        
        if not file_path.exists():
            raise HTTPException(404, f"File not found: {filename}")
        
        file_path.unlink()
        
        return {
            "status": "success",
            "message": f"Deleted {filename}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(500, str(e))

"""
Data Uploader - Upload real banking transaction data to TigerGraph
"""

import pandas as pd
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BankingDataUploader:
    """Upload banking transaction data to TigerGraph"""
    
    def __init__(self):
        self.stats = {
            'transactions': 0,
            'users': 0,
            'cards': 0,
            'merchants': 0,
            'devices': 0
        }
    
    def validate_dataframe(self, df: pd.DataFrame) -> bool:
        """Validate required columns exist"""
        required = ['transaction_id', 'user_id', 'amount']
        missing = [col for col in required if col not in df.columns]
        
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        logger.info(f"✓ Validation passed: {len(df)} records")
        return True
    
    def process_transactions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Process transaction data and prepare for upload"""
        logger.info(f"Processing {len(df)} transactions...")
        
        # Validate
        self.validate_dataframe(df)
        
        # Extract unique entities
        unique_users = df['user_id'].nunique()
        unique_merchants = df.get('merchant_id', pd.Series()).nunique()
        unique_cards = df.get('card_id', pd.Series()).nunique()
        
        self.stats['transactions'] = len(df)
        self.stats['users'] = unique_users
        self.stats['merchants'] = unique_merchants
        self.stats['cards'] = unique_cards
        
        logger.info(f"✓ Processed: {unique_users} users, {len(df)} transactions")
        
        return self.stats
    
    def upload_csv(self, filepath: str) -> Dict[str, Any]:
        """Upload CSV file with banking transactions"""
        logger.info(f"Loading CSV file: {filepath}")
        
        try:
            # Read CSV
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} transactions from {filepath}")
            
            # Process
            stats = self.process_transactions(df)
            
            # Store for later TigerGraph upload
            output_path = Path('backend/memory/uploaded_data.csv')
            output_path.parent.mkdir(exist_ok=True, parents=True)
            df.to_csv(output_path, index=False)
            
            logger.info(f"✓ Data saved to {output_path}")
            logger.info(f"✓ Upload complete: {stats}")
            
            return {
                **stats,
                'status': 'success',
                'filepath': str(output_path),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"✗ Upload failed: {e}")
            raise
    
    def upload_json(self, filepath: str) -> Dict[str, Any]:
        """Upload JSON file with transactions"""
        logger.info(f"Loading JSON file: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.json_normalize(data)
        
        # Save as CSV and process
        temp_csv = 'backend/memory/temp_upload.csv'
        df.to_csv(temp_csv, index=False)
        
        return self.upload_csv(temp_csv)
    
    def upload_directory(self, directory: str, pattern: str = "*.csv") -> Dict[str, Any]:
        """Upload all files in a directory"""
        path = Path(directory)
        files = list(path.glob(pattern))
        
        logger.info(f"Found {len(files)} files matching {pattern}")
        
        total_stats = {
            'transactions': 0,
            'users': 0,
            'cards': 0,
            'merchants': 0,
            'devices': 0,
            'files_processed': 0
        }
        
        for file in files:
            logger.info(f"Processing: {file.name}")
            try:
                stats = self.upload_csv(str(file))
                for key in ['transactions', 'users', 'cards', 'merchants', 'devices']:
                    total_stats[key] += stats.get(key, 0)
                total_stats['files_processed'] += 1
            except Exception as e:
                logger.error(f"Failed to process {file.name}: {e}")
        
        logger.info(f"✓ Total uploaded: {total_stats}")
        return total_stats


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Upload banking transaction data for fraud investigation'
    )
    parser.add_argument('--file', help='Single file to upload')
    parser.add_argument('--directory', help='Directory of files to upload')
    parser.add_argument('--pattern', default='*.csv', help='File pattern for directory')
    parser.add_argument('--type', choices=['csv', 'json'], default='csv', help='File type')
    
    args = parser.parse_args()
    
    uploader = BankingDataUploader()
    
    try:
        if args.file:
            if args.type == 'csv':
                result = uploader.upload_csv(args.file)
            else:
                result = uploader.upload_json(args.file)
            
            print("\n✓ Upload successful!")
            print(f"  Transactions: {result['transactions']}")
            print(f"  Users: {result['users']}")
            print(f"  Merchants: {result.get('merchants', 0)}")
            
        elif args.directory:
            result = uploader.upload_directory(args.directory, args.pattern)
            
            print("\n✓ Batch upload successful!")
            print(f"  Files: {result['files_processed']}")
            print(f"  Total Transactions: {result['transactions']}")
            print(f"  Total Users: {result['users']}")
            
        else:
            print("Error: Specify --file or --directory")
            parser.print_help()
            
    except Exception as e:
        print(f"\n✗ Upload failed: {e}")
        exit(1)


if __name__ == '__main__':
    main()

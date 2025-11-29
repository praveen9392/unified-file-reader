from unified_file_reader.api import read_file
from unified_file_reader import read_file
from unified_file_reader.exceptions import UnsupportedFormatError
from datetime import datetime 

if __name__ == "__main__":
    path = r"C:\Users\Praveen\Downloads\regression_training_dataset.csv"
    
    # you can use it in 2 ways 
    # first way 
    data = read_file(path)
    print(len(data))
    
    # second way 
    start_time = datetime.now() 
    try:
        result = read_file(path)
        print("=== READ SUCCESSFULLY ===")
        print(type(result))
        print(len(result))
        end_time = datetime.now()  
        print(f"Time taken: {end_time - start_time}")
    except FileNotFoundError:
        print("File not found:", path)
    except UnsupportedFormatError as e:
        print("Unsupported format:")
        print(e)
    except Exception as e:
        print("Unexpected error while reading file:")
        print(type(e).__name__, "-", e)
import os
import glob

def read_spark_conf(file_path)-> str:
    """
    Read a Spark configuration file and return a dictionary of configuration settings.
    
    Args:
        file_path (str): Path to the spark.conf file
        
    Returns:
        dict: Dictionary containing the configuration settings
    """
    config = {}
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip empty lines and comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Split by first space or tab
                parts = line.split(None, 1)
                if len(parts) == 2:
                    key, value = parts
                    config[key] = value.strip()
    except Exception as e:
        print(f"Error reading configuration file: {e}")
    
    return config

    result = []
    
    for key, value in config.items():
        # Check for keys with backticks which seem to be errors in the input dictionary
        clean_key = key.replace('`', '')
        
        # Remove any trailing colons in keys
        if clean_key.endswith(':'):
            clean_key = clean_key[:-1]
            
        # Format the configuration line
        result.append(f"--conf {clean_key}={value}")
    
    # Join all lines and remove the trailing backslash from the last line
    formatted_result = " ".join(result)
    
    if formatted_result.endswith(" \\"):
        formatted_result = formatted_result[:-2]
    
    return formatted_result
    

def read_jars_file(jar_path):
    import sys
    """
    Reads a directory containing JAR files and returns a comma-separated string of JAR file paths.
    """
    try:
        jar_files = [os.path.abspath(jar) for jar in glob.glob(os.path.join(jar_path, "*.jar"))]
        if not jar_files:
            print("Warning: No JAR files found in the specified directory.", file=sys.stderr)
            return None
        return ",".join(jar_files)
    except Exception as e:
        print(f"Error reading JAR files: {e}", file=sys.stderr)
        return None


# Example usage
if __name__ == "__main__":
    
    conf = read_spark_conf("/media/daonguyen/Dual/DataPlatform/airflow_code/config/spark.conf")
    print(conf)
    # for key, value in conf.items():
    #     print(f"{key}: {value}")
    # jarfiles = read_jars_file("/media/daonguyen/Dual/DataPlatform/airflow_code/spark_jobs/jars")
    # print(jarfiles)
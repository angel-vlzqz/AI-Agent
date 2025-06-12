from functions.write_file import write_file
from functions.run_python import run_python_file

def test_write_file():
    # Test writing to existing file
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("\nTest 1: Writing to existing file")
    print(result1)
    assert result1.startswith("Successfully wrote to")
    assert "lorem.txt" in result1
    assert "28 characters written" in result1
    
    # Test writing to new file in subdirectory
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("\nTest 2: Writing to new file in subdirectory")
    print(result2)
    assert result2.startswith("Successfully wrote to")
    assert "pkg/morelorem.txt" in result2
    assert "26 characters written" in result2
    
    # Test writing to file outside working directory
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("\nTest 3: Attempting to write outside working directory")
    print(result3)
    assert result3.startswith("Error:")
    assert "outside the permitted working directory" in result3

def test_run_python_file():
    # Test running main.py
    print("\nTest 1: Running main.py")
    result1 = run_python_file("calculator", "main.py")
    print(result1)
    assert not result1.startswith("Error:")
    
    # Test running tests.py
    print("\nTest 2: Running tests.py")
    result2 = run_python_file("calculator", "tests.py")
    print(result2)
    assert not result2.startswith("Error:")
    
    # Test running file outside working directory
    print("\nTest 3: Attempting to run file outside working directory")
    result3 = run_python_file("calculator", "../main.py")
    print(result3)
    assert result3.startswith("Error:")
    assert "outside the permitted working directory" in result3
    
    # Test running nonexistent file
    print("\nTest 4: Attempting to run nonexistent file")
    result4 = run_python_file("calculator", "nonexistent.py")
    print(result4)
    assert result4.startswith("Error:")
    assert "not found" in result4

if __name__ == "__main__":
    test_write_file()
    test_run_python_file()
    print("\nAll tests passed!") 
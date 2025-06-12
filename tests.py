from functions.write_file import write_file

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

if __name__ == "__main__":
    test_write_file()
    print("\nAll tests passed!") 
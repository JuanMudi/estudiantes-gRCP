import grpc
import students_pb2
import students_pb2_grpc

def run():
    """
    Run the client to call the server's methods
    """
    
    # Create a channel and a stub to server's IP address
    channel = grpc.insecure_channel('localhost:50020')  # Replace with the server's IP address
    stub = students_pb2_grpc.StudentServiceStub(channel)
    
    # Call GetName method
    response_name = stub.GetName(students_pb2.StudentID(id=334))
    print("Name:", response_name.full_name)
    
    # Call GetAverage method
    response_average = stub.GetAverage(students_pb2.StudentID(id=444))
    print("Average:", response_average.average)
    
    # Call GetGroup method
    response_group = stub.GetGroup(students_pb2.StudentID(id=997))
    print("Group:", response_group.group)

if __name__ == '__main__':
    run()

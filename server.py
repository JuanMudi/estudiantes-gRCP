import grpc
from concurrent import futures
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import students_pb2
import students_pb2_grpc

uri = "mongodb+srv://admin:admin@studentsdatabase.rqetwo4.mongodb.net/?retryWrites=true&w=majority&appName=studentsDatabase"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

   
    # Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
     print(e)

db = client["gRPC"]
collection = db["students"]




class StudentService(students_pb2_grpc.StudentServiceServicer):
    """
    Implements the StudentService interface defined in students.proto.
    """
    def GetName(self, request, context):
        """
        Returns the name of the student with the given id.
        
        :param students_pb2.IdRequest request: The request message containing the student id
        :param grpc.ServicerContext context: The context of the request
        """
        student_id = request.id
        data = collection.find_one({"id": student_id})

        if data is not None:
            return students_pb2.NameResponse(full_name=data["nombre"])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Student not found.")
            return students_pb2.NameResponse(full_name="")

    def GetAverage(self, request, context):
        """
        Computes the average of the two notes of the student with the given id.
        
        :param students_pb2.IdRequest request: The request message containing the student id
        :param grpc.ServicerContext context: The context of the request
        """
        student_id = request.id

        data = collection.find_one({"id": student_id})

        if data is not None:
            average = (data["taller_1"] + data["taller_2"]) / 2
            return students_pb2.AverageResponse(average=average)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Student not found.")
            return students_pb2.AverageResponse(average=0)

    def GetGroup(self, request, context):
        """
        Returns the name of the group of a student with the given id.
        
        :param students_pb2.IdRequest request: The request message containing the student id
        :param grpc.ServicerContext context: The context of the request
        """
        student_id = request.id
        data = collection.find_one({"id": student_id})

        if data is not None:
            return students_pb2.GroupResponse(group=data["grupo"])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Student not found.")
            return students_pb2.GroupResponse(group="")

def serve():

    """
    Starts the gRPC server and listens on port 50020.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    students_pb2_grpc.add_StudentServiceServicer_to_server(StudentService(), server)
    
    # Listen on all network interfaces
    server.add_insecure_port('0.0.0.0:50020')  
    server.start()
    
    print("Server started. Listening on port 50020.")
    server.wait_for_termination()

if __name__ == '__main__':
    # Starts the server
    serve()

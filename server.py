import grpc
from concurrent import futures
import students_pb2
import students_pb2_grpc

class StudentService(students_pb2_grpc.StudentServiceServicer):
    """
    Implements the StudentService interface defined in students.proto.
    """

    def __init__(self):
        """
        Class constructor. Initializes the data from file
        """
        self.student_data = self.read_student_data("students.csv")

    def read_student_data(self, filename):
        """
        Reads the student data from the file students.txt and stores it in a dictionary.
        
        :param str filename: The name of the file to read the data from.
        """
        student_data = {}
        with open(filename, "r") as file:
            next(file)  # Skip header
            for line in file:
                group, id, name, note1, note2 = line.strip().split(';')
                student_data[int(id)] = {
                    'name': name,
                    'note1': float(note1),
                    'note2': float(note2),
                    'group': group
                }
        return student_data

    def GetName(self, request, context):
        """
        Returns the name of the student with the given id.
        
        :param students_pb2.IdRequest request: The request message containing the student id
        :param grpc.ServicerContext context: The context of the request
        """
        student_id = request.id
        if student_id in self.student_data:
            return students_pb2.NameResponse(full_name=self.student_data[student_id]['name'])
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
        if student_id in self.student_data:
            average = (self.student_data[student_id]['note1'] + self.student_data[student_id]['note2']) / 2
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
        if student_id in self.student_data:
            return students_pb2.GroupResponse(group=self.student_data[student_id]['group'])
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

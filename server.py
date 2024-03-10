import grpc
from concurrent import futures
import students_pb2
import students_pb2_grpc

class StudentService(students_pb2_grpc.StudentServiceServicer):
    def __init__(self):
        self.student_data = self.read_student_data("students.txt")

    def read_student_data(self, filename):
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
        student_id = request.id
        if student_id in self.student_data:
            return students_pb2.NameResponse(full_name=self.student_data[student_id]['name'])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Student not found.")
            return students_pb2.NameResponse(full_name="")

    def GetAverage(self, request, context):
        student_id = request.id
        if student_id in self.student_data:
            average = (self.student_data[student_id]['note1'] + self.student_data[student_id]['note2']) / 2
            return students_pb2.AverageResponse(average=average)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Student not found.")
            return students_pb2.AverageResponse(average=0)

    def GetGroup(self, request, context):
        student_id = request.id
        if student_id in self.student_data:
            return students_pb2.GroupResponse(group=self.student_data[student_id]['group'])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Student not found.")
            return students_pb2.GroupResponse(group="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    students_pb2_grpc.add_StudentServiceServicer_to_server(StudentService(), server)
    server.add_insecure_port('0.0.0.0:50020')  # Listen on all network interfaces
    server.start()
    print("Server started. Listening on port 50020.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

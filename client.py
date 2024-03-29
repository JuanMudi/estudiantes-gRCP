import students_pb2
import students_pb2_grpc
import grpc

"""
Run the client to call the server's methods
"""
    
# Create a channel and a stub to server's IP address
channel = grpc.insecure_channel('52.87.167.205:50020')  # Replace with the server's IP address
stub = students_pb2_grpc.StudentServiceStub(channel)


def API(service):
        
        try:
            data = input("Ingrese el ID del estudiante: ")
        except ValueError:
            print("\nOPCIÓN INVALIDA\n")
            return


        if service == 1:
            print("Name: " + (stub.GetName(students_pb2.StudentID(id=int(data)))).full_name)
        if service == 2:
                # Check if student_id is numeric
            if data.isdigit():
                # If numeric, perform search by id
                print("Average:" + str((stub.GetAverage(students_pb2.StudentID(id=int(data)))).average))
            else:
                # If alphanumeric, perform search by name or other field
                print("Average:" + str((stub.GetAverage(students_pb2.StudentID(nombre=data))).average))
        if service == 3:       
            print("Group: " + (stub.GetGroup(students_pb2.StudentID(id=int(data)))).group)

def run():
    
    opcion = 0
    data = 0

    while True:
        print("SOLICITUD DE INFORMACIÓN\n")
        try:
            opcion = int(input("1. Obtener nombre\n2. Obtener promedio de notas\n3. Obtener grupo\n4.Salir\nPetición: "))
        except ValueError:
            print("===================================================================\n")
            print("OPCIÓN INVALIDA")
            print("\n===================================================================")
            continue
        
        if opcion == 4:
            exit(0)
             
        print("===================================================================\n")
        API(opcion)
        print("\n===================================================================")


if __name__ == '__main__':
    run()

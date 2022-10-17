from zoneinfo import available_timezones
import cv2
captured_frames = None

def list_ports():
    #from https://stackoverflow.com/questions/57577445/list-available-cameras-opencv-python
    #
    #Test the ports and returns a tuple with the available ports and the ones that are working.
    #
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port,cv2.CAP_DSHOW)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            #print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                #print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                #print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports
def can_capture():
    a_ports, w_ports, nw_ports = list_ports()
    if w_ports:
        if len(w_ports) >0:
            return True
    return False

def capture():
    port_to_use = -1
    a_ports, w_ports, nw_ports = list_ports()
    if w_ports:
        if len(w_ports) >0:
            port_to_use = w_ports[0]
        

    if port_to_use != -1: 
        cap = cv2.VideoCapture(port_to_use, cv2.CAP_DSHOW)
        while cap.isOpened():
            ret,frame = cap.read()

            if not ret:
                print("Failed to grab frame.")
                break

            #flip horizontally    
            last_frame = cv2.flip(frame,1)



            cv2.imshow('Hand Tracking', last_frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                print("frame")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Cannot capture. No port available.")





import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import time

pathSquat1 = 'videos/squat/2GJMrfFCUtM(Clip).mp4'
pathSquat2 = 'videos/squat/PwC1sKdjPSM(Clip).mp4'
pathSquat3 = 'videos/squat/t3JeDQB3Vi4(Clip).mp4'
pathSquatFromBack = 'videos/squat/TYuYICQ8HwY(Clip).mp4'

baseline = "Squat_side_view_test.mp4"
relative_path = "C:/Users/jones/OneDrive - Queen's University/4th Year/ELEC498 Capstone/Code/"

deepestLegBend = 180
deepestTorsoBend = 180
max_shoulder_disp = 0
max_knee_disp = 0

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
# VIDEO FEED
cap = cv2.VideoCapture(relative_path + pathSquat2)

first_stamp = int(round(time.time() * 1000))
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulderLeft = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hipLeft = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            kneeLeft = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankleLeft = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            shoulderRight = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            hipRight = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            kneeRight = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            ankleRight = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            #torso angles
            angleLeftShoulderHip = calculate_angle(shoulderLeft, hipLeft, kneeLeft)
            angleRightShoulderHip = calculate_angle(shoulderRight, hipRight, kneeRight)
            #leg bend angle
            angleLeftHipKneeAnkle = calculate_angle(hipLeft, kneeLeft, ankleLeft)
            angleRightHipKneeAnkle  = calculate_angle(hipLeft, kneeLeft, ankleRight)
            #print(angleLeftHipKneeAnkle)

            # # Print angles
            if(angleLeftHipKneeAnkle < deepestLegBend and angleLeftHipKneeAnkle > 20):
                deepestLegBend  = angleLeftHipKneeAnkle
            elif(angleRightHipKneeAnkle < deepestLegBend and angleRightHipKneeAnkle > 20):
                deepestLegBend  = angleRightHipKneeAnkle
            #print("Deepest leg bend:" + str(deepestLegBend))     
            

            if(angleLeftShoulderHip < deepestTorsoBend and angleLeftShoulderHip > 20):
                deepestTorsoBend  = angleLeftShoulderHip
            elif(angleRightShoulderHip < deepestTorsoBend and angleRightShoulderHip > 20):
                deepestTorsoBend  = angleRightShoulderHip
            # print("Deepest torso bend:" + str(deepestTorsoBend))
             
            if(angleLeftShoulderHip < deepestTorsoBend and angleLeftShoulderHip > 20):
                deepestTorsoBend  = angleLeftShoulderHip
            elif(angleRightShoulderHip < deepestTorsoBend and angleRightShoulderHip > 20):
                deepestTorsoBend  = angleRightShoulderHip

            print("Left Shoulder" + str(shoulderLeft[1]) )
            print("Right Shoulder" + str(shoulderRight[1]) )
            #calculate y greatest displacement in shoulder joints at a certain time 
            if((shoulderLeft[1]- shoulderRight[1]) > max_shoulder_disp):
                max_shoulder_disp = shoulderLeft[1] - shoulderRight[1]

            if((shoulderRight[1]- shoulderLeft[1]) > max_shoulder_disp):
                max_shoulder_disp = shoulderRight[1]- shoulderLeft[1]

            #calculate y greatest displacement in shoulder joints at a certain time
            # only do inwardsonly do inwardsonly do inwardsonly do inwards
            if((kneeLeft[0]- kneeRight[0]) > max_knee_disp):
                max_knee_disp = kneeLeft[0] - kneeRight[0]

            if((kneeRight[0] - kneeLeft[0]) > max_knee_disp):
                max_knee_disp = kneeRight[0] - kneeLeft[0]

            
            # print("Left shoulder-hip angle: {:.2f} degrees".format(angleLeftShoulderHip))
            # print("Right shoulder-hip angle: {:.2f} degrees".format(angleRightShoulderHip))
            # print("Left hip-knee angle: {:.2f} degrees".format(angleLeftHipKneeAnkle))
            # print("Right hip-knee angle: {:.2f} degrees".format(angleRightHipKneeAnkle))

            
        except:
            pass        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)
        second_stamp = int(round(time.time() * 1000))
        time_taken_seconds = round((second_stamp - first_stamp) / 1000)
        # print(time_taken_seconds)
        if(time_taken_seconds >= 10):         
            cap.release()
            cv2.destroyAllWindows()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
##Setup a range of angles based on squat form 

rating = ["green", "yellow", "orange", "red"]
overall = []

#Squat Depth
if(deepestLegBend <= 95):
    print("Squat depth " + rating[0])
    overall.append(4)
elif(deepestLegBend > 95 and deepestLegBend <= 110):
    print("Squat depth " + rating[1])
    overall.append(3)
elif(deepestLegBend > 110 and deepestLegBend <= 125):
    print("Squat depth " + rating[2])
    overall.append(2)
elif(deepestLegBend > 125):
    print("Squat depth " + rating[3])
    overall.append(1)

print("Squat Depth Angle " + str(deepestLegBend) + ", score " + str(overall[0]))
    
#Torso angle This only works if the video is from the side*****
# ideally the deepest part of your squat you want to have your torso 
# slightly forward 90-100 degrees any taller or more forward might casue injury

#If statement video from the side
if(deepestTorsoBend >= 90 and deepestTorsoBend <= 100):
    print("Torso position " + rating[0])
    overall.append(4)
elif((deepestTorsoBend >= 100 and deepestTorsoBend <= 125) or (deepestTorsoBend <= 90 and deepestTorsoBend >= 80)):
    print("Torso position " + rating[1])
    overall.append(3)
elif((deepestTorsoBend >= 125 and deepestTorsoBend <= 140) or (deepestTorsoBend <= 80 and deepestTorsoBend >= 70)):
    print("Torso position " + rating[2])
    overall.append(2)
elif(deepestTorsoBend < 70 or deepestTorsoBend > 140):
    print("Torso position " + rating[3])
    overall.append(1)

print("Torso Bend Angle" + str(deepestTorsoBend)  + ", score " + str(overall[1]))

#Shoulders equals
#if shoulders are even in height from the front throughout the movement
if(max_shoulder_disp < 0.02): # range with slight angulature nothing to be concerned about
    print("Shoulder Disp " + rating[0])
    overall.append(4)
elif(0.02 <= max_shoulder_disp < 0.04 ):
    print("Shoulder Disp " + rating[1])
    overall.append(3)
elif(0.04 <= max_shoulder_disp < 0.08):
    print("Shoulder Disp " + rating[2])
    overall.append(2)
elif(0.08 <= max_shoulder_disp):
    print("Shoulder Disp " + rating[3])
    overall.append(1)

print("Max Shoulder Disp:" + str(max_shoulder_disp)  + ", score " + str(overall[2])) 

#Knees inwards
# same calculation for knee displacment from the front
if(max_knee_disp < 0.02): # range with slight angulature nothing to be concerned about
    print("Knee Disp " + rating[0])
    overall.append(4)
elif(0.02 <= max_knee_disp < 0.04 ):
    print("Knee Disp " + rating[1])
    overall.append(3)
elif(0.04 <= max_knee_disp < 0.08):
    print("Knee Disp " + rating[2])
    overall.append(2)
elif(0.08 <= max_knee_disp):
    print("Knee Disp " + rating[3])
    overall.append(1)

print("Max Knee Disp:" + str(max_knee_disp)  + ", score " + str(overall[3])) 



#Head position

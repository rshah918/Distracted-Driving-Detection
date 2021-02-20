# Distracted-Driving-Detection
A machine learning based system for driver awareness monitoring

# Software Workflow: 
1: Take in camera input
    -OpenCV allows us to do this easily
    
2: Detect Faces  
    -Haarcascade
    
3: Detect Eyes  
    -Mobilenet SSD
    
4: Classify Eyes as open/closed  
    - Custom classifier network in Tensorflow  
    
5: Detect Distraction Event  
    -If an eye is closed for too long, raise a distraction event
    
5: Raise an audible/visual alert  
    -Send message to Arduino

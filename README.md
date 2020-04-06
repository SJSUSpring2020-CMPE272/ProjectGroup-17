

## Traffic Governance System

### Project Idea Description: -
Traffic system shows a great scope of trade with the environment and is directly connected to it. Manual traffic systems are proving to be insufficient due to rapid urbanization. Central monitoring systems are facing scalability issues as they process increasing amounts of data received from hundreds of traffic cameras. Major traffic problems like congestion, safety, pollution (leading to various health issues) and increased need for mobility. A solution to most of them is the construction of newer and safer highways and additional lanes on existing ones, but it proves to be expensive and often not feasible. Cities are limited by space and construction cannot keep up with ever-growing demand. Hence a need for an improved system with a minimal manual interface is persisting. Smart traffic governance system uses Artificial Intelligence to determine the flow of traffic, automated enforcement and communication to change the face of the traffic scenarios in urban cities suffering from such traffic issues.
Traffic governance system will deal with the traffic on the crossroads with the help of cameras on the crossroads which will detect the congestion with the help of image processing and get the count of vehicles in the heavy lane. After detecting the heavy lane, the timer for that particular will increase and the other lanes timer will be balanced accordingly.

### Goal: 
The scope of this project is very vast; people travelling long distances will be benefited the most by this application as the travel time will be greatly reduced.
People travelling in the day to day life for work will also be benefited by reducing the waiting time on the signals. It will help to create fewer congestion on the crossroads and the heavy lane.

### Technology Stack:
Frontend: - HTML, CSS, Bootstrap, JS <br>
Database: - Mysql <br>
Backend and Tools: - Python, OpenCV, Flask (Framework), MatplotLib


### Class Diagram:
There two main class Admin and Police Staff.<br>
- The admin has functionalities like Adding Staff members, altering timer, etc.
- The Police Staff members can request for reports , add feedback , etc.

![e8e2e2fa-1592-43fc-8f44-96c0b04220a4](https://user-images.githubusercontent.com/29951473/78604307-7cfc3480-780e-11ea-9312-5f197de36680.jpg)


### System Flow Diagram:
As shown in the flow diagram, Admin will be responsible for adding new dataset, generating reports and alter traffic timer, whereas Police Staff will be responsible for adding new complaints and giving feedback.

![System Flow](/images/SystemFlowDiagram.jpeg)


### Data Flow Diagram:

Following picture shows how the data will flow in the system.
Admin is termed as the actor or user whereas Tables on the rightmost side are data stores. Round objects are the procedures that are executed by admin on data store to manipulate data.

So, as shown admin can Organize staff by adding, updating or deleting, Regulate dataset by adding new data in terms of frames to the system, Alter signal timer according to the results of detection.
Apart from these admin can generate report, view and acknowledge to complaints and feedback posted by user.

![4](https://user-images.githubusercontent.com/46435796/78605973-60adc700-7811-11ea-9529-553d0bab0d6d.jpg)


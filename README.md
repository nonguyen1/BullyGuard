# BullyGuard

## Inspiration 
As the internet becomes increasingly prevalent in society, social media outlets follow. With these outlets the world begins to feel more interconnected as people from across the globe start to meet at the touch of their fingers. Though with the anonymity that comes with these outlets a lot of toxicity follows. This has led to the creation of cyber bullying. Cyber bullying is a serious issue that is often overlooked by many due to its deviation from traditional physical bullying. Though the emotional damage cyberbullying causes can arguably be considered on par or worse that than of physical harm. As such we decided that we should address this issue through a coding program which we wanted to demo at the hackathon.

## What it does
BullyGuard is a program that utilizes a machine learning model to analyze texts sent through a discord chat lobby. These texts are classified as either bullying like or not. Those who have sent bullying like messages will then be graded on the severity of their statements and a rank will be assigned to them to rate how toxic they are as people. This will allow other members to recognize how toxic certain chat lobbies are, and inform them to avoid it if possible.

## How I built it
We found and cleaned cyberbullying datasets from Formspring and Bayzick. We used these datasets to build using a logistic regression filtered through a 2 gram model. This model was used to analyze online test data which allowed it to learn different bullying phrases. We also developed several discord bots. These bots partnered with the model analyzes texts in the chat lobby and ranks the severity of each text in terms of bullying.

## Challenges I ran into
The original path that this project was taking was to use aws online deep learning model to analyze the data. Though the server at aws was taking an excessively long time and as such the idea had to be scrapped along with a majority of the team’s motivation. At this point we had planned to drop from the hackathon, but in the end rebounded by creating our own machine learning model in the remaining time.

## Accomplishments that I'm proud of
We are relatively proud of how we decided to stay in the competition despite the major setback we encountered. We were able to make due with the code we already wrote, and after several debugging errors we were able to complete the project.

## What I learned
From this experience many things were learned. Things such as what makes a good deep learning model, as well as how discord bots are made and function. I personally learned a lot about backends and connecting to an online network and server. I suppose the biggest lesson although cliche was determination and motivation.

## What's next for BullyGuard
We plan to expand the program by applying it to more than a single discord chat lobby at a time. Rather we want the program to be able to run on multiple chat lobbies and rank each lobby by how toxic it is, so people know what they are getting themselves into. We also want to implement an even more comprehensive machine learning model to make predictions and rankings more accurate. After this hopefully the program can expand to all social media platforms, thereby increasing awareness about the pressing issue of cyber bullying as well as acting as a deterrent to those who would conduct this action.

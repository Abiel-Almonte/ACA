
# Assistant College Advisor (ACA)

An AI app that provides a concierge service that help students find all the information they need to make informed decisions when selecting their courses.
Designed and deployed a scalable API serving an in-house LLM with a real time chat interface fostering a dynamic and interactive experience for users.

## Key Features
1. **Personalized Recommendations**: The chat bot can analyze students' given academic performance, interests, and career goals to provide tailored course recommendations. By understanding each student's unique needs, the bot can suggest courses that align with their academic and professional objectives.

2. **Real-Time Assistance**: Students can receive instant assistance and answers to their queries about courses, schedules. This ensures that students have access to support whenever they need it, facilitating quick decision-making during the course selection process.

3. **Interactive Experience**: The chat bot can engage students in interactive conversations, guiding them through various aspects of course selection such as exploring different majors and understanding course requirements. This interactive experience makes the process more engaging and enjoyable for students, enhancing their overall satisfaction.

4. **Information Accessibility**: The AI app can aggregate and present information from various sources such as course & faculty catelogs, and peer reviews in a user-friendly format. This enables students to access comprehensive information about courses, including descriptions, instructor profiles, and student feedback, all within the chat interface.

5. **Scalability and Efficiency**: By deploying a scalable API, idealy the AI app can handle a large volume of requests from students without compromising performance. This ensures that students receive prompt assistance and support, even during peak periods of course selection.

6. **Dynamic Retrieval-Augmented Generation (RAG)**: My approach to driving the entire interaction between the LLM and the user involves utilizing a retriever module, if deemed necessary by the LLM, to select documents from a knowledge source based on the user's query, employing a vector database. These documents, once retrieved, act as context for the LLM to generate a response that is both coherent and contextually relevant.

    |![Dynamic RAG](./media/logic_workflow.png "Implmented in logic.py")|
    |:--:|
    |*My code implmentation of "dynamic" RAG: ```./server/logic/logic.py```*|

## Demo
![Demo](./media/Fullstack_Update2.gif)

>**Note**:
>Currently employing an unfinished dataset.

## Future Additions
1. **Docker Container**

2. **Completed Dataset**:
    - **Professor Profile** (In Progress)
        - Biography
        - Research & Educational Interests
        - Degrees
        - Websites
    - **Ratings** (Done)
        - Student Perception of Teaching  (SPoT) surveys
            - A short paper explaining how the ratings were created is located in  ```./media/Ratings_Paper.pdf```
    - **Class Details** (Done)
        - Weekly Schedule
        - Location
    - **Course information** (In Progress)
        - Course Description 

>**Note**: 
>Althogh parts are done, the are still not integrated.

## Current App Structure

**Client:** React.js

**Server:** Websocket, FastAPI, Ray Serve, vLLM, Milvus, Docker, Langchain, HuggingFace


## Deployment

To deploy this project run

```bash
  git clone https://github.com/Abiel-Almonte/ACA.git
  cd ACA/server/milvus
  docker compose up -d
  cd ../
  serve run config.yaml
  cd ../client
  npm start
```
>**Note**: 
>Must download and AWQ quantize Mistral 7B \
>**WARNING**:
>Must have at least 6GB of VRAM

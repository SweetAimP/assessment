# assessment
Data Engineer Assessment

# Explation
In this repo you will find three different folders, **airflow**,**flask_app** and **inputs**, also you will find at the main level **docker-compose.yaml** file with the *definition* for all the containers used for this solution, Postgres container playing as "Data warehouse", Flask api container used for the *API*, **etc.**


* **Airflow** --> folder dedicated to the end-to-end data pipeline
  * **dags** --> Here you find one additional folder named **queries**
      * **queries** Cointains multiple python files that export variables as queries used in the different steps
      *  **dags.py** Dag definition for airflow
  * **outputs** --> is the folder used for the last step (Export report) used to store the csv file created for Finance
    
* **Flask_app** --> folder dedicated to the API Development
    * **DockerFile** File to build the custome Docker Image used for the API
    * **requirements** File with all the dependecies needed to run the solution
    * **connection** Python file to create the database Connection (Postgres Container (DB-1)(this one is different to the postgrest container used for airflow itself)
    * **dataClase** Python file with the DataClass definition used to map the objects (Product, Metadata)
    * **summary** Pythn file with the Object definition for each response (Cancelled, Shipped/Success)
    * **service** Python file that works as man in the midle, handles the first contact from the controler (app.py) and the responses from the repository, this one is in charge of build the Summary(serialize)
    * **repository** Python file specialized on handling the last interactions during the request, in this case, in charge of hanlding database request/response
    * **app.py** main file to run the API(Controller) simple in charge of leting in all the requests and returning the response
  
* **Inputs** --> Here you could find the files used as inputs(Raw Data)
    * I did include a new file ( **Platform_fees.csv** ) that is used as Dimension to keep some data referenced without having to modifed the queries.

* **Additional findings elements withint the process:**
    * As some of the files (**Graded_products.csv - Grading_fees.csv**) had differente datatype or column configuration (Upper/Lower) in some of the SQL Scripts I'm using UPPER() to ensure that all the data is used in the final report.
    * within the process I created a "Slowly Change Dimension" to keep record of the last_update field, this step is created with a **MERGE**, the final date used for the report comes from this dimension/table
    * As part of the process, there is a step that homologates the values for the countries as some of the countries are no present in the *transport_cost.csv*, avoiding with this having hardcoded values.

# How to...

To be able to run this solution you will need to have Docker Desktop install, as this solution is dockerized. Once you have check you already have Docker you can follow the next steps:
1. **clone the repo**
2. **Build the API Image** from the root folder level of the repo you can build the image used for the API container with the following command. *build -f .\flask_app\DockerFile -t flask_api .\flask_app\* this command will build the image referenced in the docker-compose.yaml.
3. **From the root folder** level of the repo execute the next command *docker compose up -d* this command with start deploying the containers.
4. **Once everything is up** you can access airflow webserver *http://localhost:8080* there you will find 3 dags paused.
5. **Unpause the dags**
6. **Execute** only the dag called ***create_tables***, this dag is configured to trigger the other two dags, they have a explicit dependency (for this solution I found it accurate to show, how you can call multiple dags depending on the final state of other dag using Sensors)
7. **Once finished** the execution of the dag called *finance report* you can go to the Output folder, there should be the csv generated for the Finance Report.
8. **(Optional)** if you want to check the tables created during the process you can login to the adminer( *http://localhost:8088/* ) I did include in the *docker-compose.yaml*
9. **API Check** Now that everything has finished and the tables are ready you can curl the API Server to list items using the *License_plate* using the following structure (**curl http://127.0.0.1:5000/v1/item/BW221109148489**), in case you try to request with a License_plate not found you will get a "No record found" response.

# Co-Author Newtork
  This network science project enables the user to visualize a newtork in which every selected scientific author is connected to each one of his/her coauthor.
  To implement this I used the following python modules:
  * matplotlib: for data visualization
  * networkx: for the newtork management
  * PIL and urlib: for downloading images from the net
  * scholarly: for scraping google scholar in search of authors
  * psycopg2: for the database management



![Output Example](/assets/images/example1.png)

![Output Example](/assets/images/example2.png)



### Note: I used a database to speed up the process of searching authors
The core operation of the algorithm is to find an author and all of his/her coauthor. The best way to do so is using the google scholar scraper but it can be really slow sometimes so I created a db that stores all the previous searches so that the second time a name appears the search is as fast as possible.

### How to use the program
There are few steps you need to do in order to be able to run the program successfully:
* make sure python3 is installed on your device. Otherwise consult the official [website](https://www.python.org/about/gettingstarted/)
* install the following libraries:
    * matplotlib
    * newtorkx
    * scholarly
    * psycopg2
* install and setup postgreSQL. If you need help follow this [guide](https://www.prisma.io/dataguide/postgresql/setting-up-a-local-postgresql-database)
* transfer the ProjectErdos.sql into your postgres server
* run the program by typing "python3 main.py"

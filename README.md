# iBills
A simple locally-hosted web-based Online Billing System implementing the Python Flask framework while using HTML and CSS for the webpages and XAMPP MySQL for the database.

This project was a group effort that was submitted on Sep 22, 2022 as a Final Project requirement during my 3rd year in College.

## About
In the recent century, waste paper has been a problem for individuals and the environment. Thus, the researchers developed an online platform for all bills that provides online payment, bill organization, and access to transaction history that will limit the creation of paper and the inconvenience that transportation brings. The application developed can register users into the platform on where they can view the details of an ongoing bill and pay it using a wide variety of payment options. Bill Providers can also use the platform as means to deliver bill details and validate transactions. To develop the application, the Python Flask framework was implemented which was connected to a MySQL database. The developers, therefore, conclude that this application will not only help contribute to the reduction of paper waste and pollution but will also protect consumers and workers in the sector from such dangerous chemicals. It will also improve the convenience and comfortability of customers using the all-in-one application as they do not leave the vicinity to pay their bills.

## Objectives
The study aims to develop an online platform for all bills that provides online payment, bill organization, and access to transaction history
The specific objectives are the following:
- Reduce the overproduction of paper by implementing online billing instead of paper billing
- Strengthen information security and avoid information leakage of customer information from bills.
- Provide convenience to customers by having a wide variety of payment options instead of going to physical payment centers which would consume a lot of time.
- Increase the preference of customers to access and pay their bills via online billing instead of the traditional way.
- Reduce the threat of hazardous chemicals such as BPA and BPS to customers and members involved in the industry.

## Significance
The system of this project will focus on the benefits that are being given to the following individuals:
- **For Corporate Companies.** This project will benefit corporate Companies in terms of having a simple, straightforward, and efficient billing application for its customers. It also provides a good value for your customers since they don’t have to go outside most of the times just so they can pay their bills to each associated company.
- **For Customers.** It benefits the customers greatly since the program offers not one, but many billing statements from different companies with just a tap on the screen.
- **For the environment.** This project benefits the environment by lessening the amount of paper bills being mailed to customers’ homes, reducing the cutting down of trees in order to make paper therefore making the application environmentally friendly all the while being convienient
- **For Future Developers.** Other developers may be able to use this application/study in the future as a reference/guide if ever they are going to be constructing a similar application or case study. This study will contribute to Information and Communications Technology in providing an alternative way in checking grammar. Lastly, this study can use as a future reference or works in other capstone/thesis.

## Scope and Delimitations
### Scope
The application will be able to:
**User:**
- Show ongoing bills and transaction history
- Show total amount of bills to pay and bill with the nearest deadline
- See the details of an ongoing bill and pay it.
- Change their profile at any time
**Bill Provider:**
- List all registered users
- Create new bill and send it to a user
- Validate paid bills of a user
**Admin:**
- Create Bill Provider accounts
- Remove all type of accounts

### Delimitations
The application will be limited to the following extent:
- It will only be available on the Windows platform
- It will only provide service to registered users and bill providers
- It can only be run locally using a command prompt under the command ‘python app.py’
- The database can only be accessed through XAMPP MySQL

## Materials
### Software
The software used to develop the platform is Visual Studio Code. The developers used the Python language to implement the Flask framework and HTML and CSS as with the help of Adobe Photoshop for the system design. The Python under the Flask framework acted as the Back End of the system which connected the pages involved while the HTML was responsible for creating the Front End of the system on where CSS was used to design and stylize and help make an interactive user interface. The programmers also use the application called XAMPP that is responsible for manipulating the data using the MySQL database. The Command Prompt was also used to run the program locally.

### Use Case
<img src="/screenshots/UseCase.png" width=50% height=50%>

### Data Model
<img src="/screenshots/DataModel.png" width=50% height=50%>

## Project Screenshots
<img src="/screenshots/HomeScreen.png" width=75% height=75%>

### Customer
<img src="/screenshots/CustomerSignInScreen.png" width=75% height=75%>
<img src="/screenshots/CustomerSignUpScreen.png" width=75% height=75%>
<img src="/screenshots/CustomerMainMenu.png" width=75% height=75%>
<img src="/screenshots/CustomerBillingDetails.png" width=75% height=75%>
<img src="/screenshots/CustomerPaymentHistory.png" width=75% height=75%>

### Bill Provider
<img src="/screenshots/BillProviderOngoingBills.png" width=75% height=75%>
<img src="/screenshots/BillProviderTransactionHistory.png" width=75% height=75%>
<img src="/screenshots/BillProviderGenerateBill.png" width=75% height=75%>
<img src="/screenshots/BillProviderValidatePayments.png" width=75% height=75%>

### Admin
<img src="/screenshots/AdminMainMenu.png" width=75% height=75%>
<img src="/screenshots/AdminCreateBillProvider.png" width=75% height=75%>

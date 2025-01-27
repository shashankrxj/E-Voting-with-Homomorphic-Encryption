# Introduction
The E-Voting with Homomorphic Encryption in Cloud project is an innovative web development application that enhances the security and privacy of electoral processes through advanced cryptography. This online voting system ensures voter confidentiality by using homomorphic encryption to enable votes to be cast and counted without disclosing individual choices.  The project utilizes a cloud-based MongoDB database to securely store user credentials and encrypted votes, enabling efficient management by administrators. This project intends to offer a strong and user-friendly platform for holding elections while preserving the secrecy and integrity of the voting process, with separate user roles for administrators, candidates, and voters.

When a vote is cast, it is added to the candidate's existing encrypted vote count in real-time. The administrator's sole responsibility is to decrypt the final tally using their private key, ensuring the confidentiality of individual votes. This real-time vote aggregation distinguishes this project from others in the field.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation & Setup](#installation--setup)
4. [Usage Guide](#usage-guide)
5. [Roles](#roles)
6. [Result](#result)
7. [Scalability Analysis](#scalability-analysis)
8. [License](#license)
9. [Contributing](#contributing)

## Features

- **Secure Voting Process**: Utilizes homomorphic encryption to maintain voter confidentiality while allowing votes to be counted without revealing individual choices.
- **Real-Time Vote Aggregation**: Votes are added in real-time to the candidate's existing encrypted vote count, ensuring up-to-date results.
- **Role-Based Access Control**: Differentiates user roles for administrators, candidates, and voters, enhancing security and user management.
- **Cloud-Based Database**: Employs MongoDB for secure storage of user credentials and encrypted votes, providing reliable data management.

## Technologies Used

- **Programming Languages**: Python, JavaScript
- **Frameworks**: Flask for web development
- **Database**: MongoDB for cloud-based data storage
- **Cryptography**: Paillier homomorphic encryption for secure voting

## Installation & Setup

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/shashankrxj/E-Voting-with-Homomorphic-Encryption.git

2. Navigate to the project directory:
   ```bash
   cd E-Voting-Homomorphic-Encryption-Cloud

3. Set up your MONGO_URI and SECRET_KEY
   ```bash
   MONGO_URI = Your MONGO_URI in db.py file for having database connection
   SECRET_KEY = Your SECRET_KEY in app.py for having session management

5. Install the required packages:
   ```bash
   pip install -r requirements.txt

## Usage Guide

- **Register Users**: Use the registration routes to create administrator, candidate, and voter accounts.
- **Casting Votes**: Voters log in, select their candidate, and cast an encrypted vote.
- **Tallying Votes**: Administrators can calculate the election results by decrypting the vote totals and viewing the results.
- **Resetting the Election**:Use the reset button to clear votes and reset the database for a new election.

## Roles

1. **Administrator**
   - **Tally Votes**: Calculates and decrypts the total votes to obtain election results.
   - **Oversee Elections**: Initiates new elections and resets the voting process when necessary.

![admin_dashboard](https://github.com/user-attachments/assets/ac20bdf3-cd8a-4fb1-a118-e48d35dbd241)
This Image shows the Calculated Results.
    

2. **Candidate**
   - **Run for Election**: Participates in elections as a candidate after registering themselves.
   - **View Results**: Accesses their own voting results after the tally is completed.
  
![Candidate_dashboard](https://github.com/user-attachments/assets/6390807e-a639-45b7-92cf-cd8b4c1f499b)
This Image showing the number of vote the Individual candidate has got.


3. **Voter**
   - **Cast Vote**: Securely logs in to cast their vote for their preferred candidate.
   - **Voting Status**: Maintains a record of voting to ensure they can only vote once per election.

![voter_dashboard](https://github.com/user-attachments/assets/e283a372-5340-4d2a-bf11-ada9dce313b8)
This Image shows the option of candidates to vote.

## Result

![Image](https://github.com/user-attachments/assets/cf561629-8c58-463f-8090-e09b7e39e9df)

This table provides performance metrics for an E-voting system implemented with homomorphic encryption. The results were obtained by running the system with 10 candidates and varying the number of votes cast. The primary focus is on three performance indicators:

1. **Average Encryption Time (ms)**: This measures the time required to encrypt a single vote. As the number of votes increases, the encryption time slightly grows, reflecting the added computational overhead due to the volume of data being processed. For example, encrypting 100 votes takes an average of 433.45 ms, while encrypting 1000 votes requires 572.39 ms.

2. **Average Update Time (ms)**: This represents the time required to update the aggregated encrypted vote data (such as adding a new encrypted vote to the tally). The system demonstrates efficient performance here, with negligible growth in update time as the number of votes increases. For instance, updating for 100 votes takes only 0.03 ms, compared to 0.17 ms for 1000 votes.

3. **Decryption Time (ms)**: This shows the time required to decrypt and tally the votes. Decryption time increases with the number of votes cast, highlighting the computational demand for larger datasets. The time rises from 89.83 ms for 100 votes to 163.61 ms for 1000 votes.

### Graphical Representation

![Image](https://github.com/user-attachments/assets/cb98c6cd-b175-46fb-a4d3-3b5c49a8b87a)

## Scalability Analysis

The scalability of this E-voting system is evident from its performance metrics:

1. **Linear Encryption Performance**: The encryption time grows proportionally with the number of votes, ensuring predictable performance as voter turnout increases.
   
2. **Minimal Update Overhead**: Real-time vote aggregation is highly optimized, resulting in almost negligible update times regardless of vote volume. This makes the system suitable for high-turnout elections.
 
3. **Acceptable Decryption Time**: While decryption time increases with the dataset size, the performance remains within practical limits for most electoral scenarios.

This system is well-suited for elections of varying sizes, from small-scale organizational votes to large national elections. However, further optimizations in encryption and decryption algorithms may be required for extremely large datasets to minimize computation time further.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome and encouraged! If you would like to help improve this project, please follow these steps:

1. **Fork the Repository**: Click on the "Fork" button at the top of this page to create a copy of this repository under your GitHub account.
2. **Clone the Forked Repository**: Clone your forked repo to your local machine.
3. **Pull Request**: After valid updation submit a pull request.

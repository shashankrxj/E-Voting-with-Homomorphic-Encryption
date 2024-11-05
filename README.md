# Introduction
The E-Voting with Homomorphic Encryption in Cloud project is an innovative web development application that enhances the security and privacy of electoral processes through advanced cryptography. This online voting system ensures voter confidentiality by using homomorphic encryption to enable votes to be cast and counted without disclosing individual choices.  The project utilizes a cloud-based MongoDB database to securely store user credentials and encrypted votes, enabling efficient management by administrators. This project intends to offer a strong and user-friendly platform for holding elections while preserving the secrecy and integrity of the voting process, with separate user roles for administrators, candidates, and voters.

When a vote is cast, it is added to the candidate's existing encrypted vote count in real-time. The administrator's sole responsibility is to decrypt the final tally using their private key, ensuring the confidentiality of individual votes. This real-time vote aggregation distinguishes this project from others in the field.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation & Setup](#installation--setup)
4. [Usage Guide](#usage-guide)
5. [Roles](#roles)
6. [License](#license)
7. [Contributing](#contributing)

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

![admin_dashboard](https://github.com/user-attachments/assets/9b58639e-6f1b-4422-a3d2-5ffdda01bc95)
This Image shows the Calculated Results.
    

2. **Candidate**
   - **Run for Election**: Participates in elections as a candidate after registering themselves.
   - **View Results**: Accesses their own voting results after the tally is completed.
  
![candidate_dashboard](https://github.com/user-attachments/assets/7d95f0e0-2f51-4e79-93e9-2cd7ae8acda6)
This Imgae showing the number of vote the Individual candidate has got.


3. **Voter**
   - **Cast Vote**: Securely logs in to cast their vote for their preferred candidate.
   - **Voting Status**: Maintains a record of voting to ensure they can only vote once per election.

![voter_dashboard](https://github.com/user-attachments/assets/de0e1106-4e6f-4f68-86ac-d01f5bd25243)
This Imgae shows the option of candidates to vote.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome and encouraged! If you would like to help improve this project, please follow these steps:

1. **Fork the Repository**: Click on the "Fork" button at the top of this page to create a copy of this repository under your GitHub account.
2. **Clone the Forked Repository**: Clone your forked repo to your local machine.
3. **Pull Request**: After valid updation submit a pull request.

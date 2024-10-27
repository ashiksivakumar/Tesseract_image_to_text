<?php
// Replace these values with your actual database credentials
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "text_extraction_app1";

// Create a connection to the database
$conn = new mysqli($servername, $username, $password, $dbname);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Process form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $fname = $_POST["fname"]; // Use the correct key for First Name
    $lname = $_POST["lname"]; // Use the correct key for Last Name
    $email = $_POST["email"]; // Use the correct key for Email id
    $password = $_POST["password"]; // Use the correct key for Password

    // Use prepared statements to insert data into the database
    $sql = "INSERT INTO userdb (fname, lname, email, passwd) VALUES (?, ?, ?, ?)";

    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssss", $fname, $lname, $email, $password);

    if ($stmt->execute()) {
        echo "Registration successful";
    } else {
        echo "Error: " . $stmt->error; // Print the specific error
    }
    

    $stmt->close();
}

// Close the database connection
$conn->close();
?>

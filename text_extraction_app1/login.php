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

    $username = $_POST["username"];
    $password = $_POST["password"];

    // Check if the username exists in the users dictionary and if the provided password matches
    $sql = "SELECT * FROM userdb WHERE email='$username' AND passwd='$password'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        echo "Login successful";
    } else {
        echo "Invalid credentials. <a href='/'>Try again</a>.";
    }
}

// Close the database connection
$conn->close();
?>

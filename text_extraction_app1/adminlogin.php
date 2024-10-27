<?php
// ... (previous code)

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    // Use prepared statements to prevent SQL injection
    $stmt = $conn->prepare("SELECT * FROM admin WHERE username = ? AND password = ?");
    $stmt->bind_param("ss", $username, $password);

    // Execute the query
    $stmt->execute();

    // Get the result
    $result = $stmt->get_result();

    // Check if a row was returned (login successful)
    if ($result->num_rows > 0) {
        header("Location: admin.php"); // Redirect to admin page
        exit();
    } else {
        echo "Invalid credentials. <a href='/'>Try again</a>.";
    }

    $stmt->close();
}

// ... (remaining code)
?>

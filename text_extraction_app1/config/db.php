<?php
$con = mysqli_connect("localhost", "root", "", "text_extraction_app1");

// Check connection
if (!$con) {
    die("Connection failed: " . mysqli_connect_error());
}

// Example SQL query
$sql = "SELECT * FROM your_table";
$result = mysqli_query($con, $sql);

if ($result) {
    while ($row = mysqli_fetch_assoc($result)) {
        // process rows
    }
} else {
    echo "Error: " . mysqli_error($con);
}

mysqli_close($con);
?>

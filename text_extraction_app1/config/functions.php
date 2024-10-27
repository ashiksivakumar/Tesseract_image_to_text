<?php 

  require_once 'db.php';

  function display_data(){
    global $con;  // Add this line to use the global connection variable
    $query = "select * from feedback";
    $result = mysqli_query($con, $query);
    return $result;
  }

?>

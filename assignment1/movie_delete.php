<?php
    require_once "functions.php";

    if (isset($_GET['id']))
        deleteMovie($_GET['id']);

    header('Location: index.php');
?>
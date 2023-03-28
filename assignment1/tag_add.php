<?php
    session_start();

    require_once "tag_form.php";
    require_once "functions.php";

    if (isAddTagPost($_POST)) {
        $errors = validateTagForm($_POST);
        if (empty($errors)) {
            insertTag($_POST['userId'], $_POST['movieId'], $_POST['tag'], time());
            header("Location: movie.php?id=".$_POST['movieId']);
        }
        else {
            // display errors
        }
    }
    else {
        $userId = '';
        $movieId = '';

        if (isset($_SESSION['userId']))
            $userId = $_SESSION['userId'];
            
        if (isset($_GET['movieId']))
            $movieId = $_GET['movieId'];

        getTagForm($userId, $movieId);
    }
?>
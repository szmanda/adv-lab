<?php
    require_once "functions.php";
    require_once "tag_form.php";

    if (isset($_GET['userId']) && isset($_GET['movieId']) && isset($_GET['tag'])) {
        $errors = validateTagForm($_POST);
        if (empty($errors)) {
            deleteTag($_GET['userId'], $_GET['movieId'], $_GET['tag']);
            header("Location: movie.php?id=".$_GET['movieId']);
        }
    }
    header('Location: movie.php?id='.$_GET['movieId'].'&error=1');
?>
<?php
    require_once "functions.php";

    if (isset($_GET['id'])) {
        $id = $_GET['id'];

        $movie = getMovie($id);
        $ratings = getMovieRatings($id, 0, 2);
        $tags = getMovieTags($id, 0, 3);

        foreach ($movie as $key => $value) {
            echo "Key: $key; Value: $value<br>";
        }

        foreach ($ratings as $rating) {
            echo "Rating: <br>";
            foreach ($rating as $key => $value) {
                echo "Key: $key; Value: $value<br>";
            }
            echo "<br>";
        }

        foreach ($tags as $tag) {
            echo "Tag: <br>";
            foreach ($tag as $key => $value) {
                echo "Key: $key; Value: $value<br>";
            }
            echo "<br>";
        }
    }
    else {
        header('Location: index.php');
    }
?>
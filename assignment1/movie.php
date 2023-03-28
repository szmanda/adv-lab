<?php
    include("header.php");
    require_once "functions.php";

    if (isset($_GET['id'])) {
        $id = $_GET['id'];

        $movie = getMovie($id);
        $ratings = getMovieRatings($id, 0, 5);
        $tags = getMovieTags($id, 0, 3);

        ?>
            <h1><?php echo $movie["title"] ?></h1>
            <h3><?php echo $movie["genres"] ?></h3>
            <a class="btn btn-outline-primary" href="movie_edit.php?id=<?php echo $id?>" role="button">Edit movie</a>
            <a class="btn btn-outline-danger" href="movie_delete.php?id=<?php echo $id?>" role="button">Delete movie</a>
            <br>

            <h2>Ratings</h2>
            <a class="btn btn-outline-primary" href="rating_add.php?movieId=<?php echo $id?>" role="button">Add rating</a>
            <table class="table">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Rating</th>
                <th scope="col">User ID</th>
                <th scope="col">Date</th>
                <th scope="col">&nbsp;</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    for ($i = 0; $i < count($ratings); $i++) {
                ?>
                        <tr>
                        <th scope="row"><?php echo $i ?></th>
                        <td><?php echo $ratings[$i]["rating"] ?></td>
                        <td><?php echo $ratings[$i]["userId"] ?></td>
                        <td><?php echo $ratings[$i]["timestamp"] ?></td>
                        <td><a class="btn btn-outline-danger" href="rating_delete.php?userId=<?php echo $ratings[$i]["userId"]?>&movieId=<?php echo $id?>&rating=<?php echo $ratings[$i]["rating"]?>" role="button">Delete</a></td>
                        </tr>
                <?php
                    }
                ?>
            </tbody>
            </table>

            <h2>Tags</h2>
            <a class="btn btn-outline-primary" href="tag_add.php?movieId=<?php echo $id?>" role="button">Add tag</a>
            <table class="table">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Tag</th>
                <th scope="col">User ID</th>
                <th scope="col">Date</th>
                <th scope="col">&nbsp;</th>
                </tr>
            </thead>
            <tbody>
                <?php
                    for ($i = 0; $i < count($tags); $i++) {
                ?>
                        <tr>
                        <th scope="row"><?php echo $i ?></th>
                        <td><?php echo $tags[$i]["tag"] ?></td>
                        <td><?php echo $tags[$i]["userId"] ?></td>
                        <td><?php echo $tags[$i]["timestamp"] ?></td>
                        <td><a class="btn btn-outline-danger" href="tag_delete.php?userId=<?php echo $tags[$i]["userId"]?>&movieId=<?php echo $id?>&tag=<?php echo $tags[$i]["tag"]?>" role="button">Delete</a></td>
                        </tr>
                <?php
                    }
                ?>
            </tbody>
            </table>
        <?php
    }
    else {
        header('Location: index.php');
    }
?>
<?php
    require_once "functions.php";
    function getMovieForm($id = -1) {
        $update = $id == -1 ? false : true;
        $title = '';
        $genres = '';
        if ($update) {
            $movie = getMovie($id);
            $title = $movie['title'];
            $genres = $movie['genres'];
        }
        include("header.php");
        ?>
        <div class="col-8">
            <form action=<?php ($update) ? (print "movie_edit.php") : (print "movie_add.php"); ?> method="post">
                <div class="mb-3">
                    <label for="title" class="form-label">Title</label>
                    <input type="text" class="form-control" name="title" id="title" value="<?php echo $title?>">
                </div>
                <div class="mb-3">
                    <label for="genres" class="form-label">Genres</label>
                    <input type="text" class="form-control" name="genres" id="genres" value="<?php echo $genres?>">
                </div>
                <?php
                    if ($update) {
                        ?>
                            <input name="id" id="id" value="<?php echo $id?>" type="hidden">
                        <?php
                    }
                ?>
                <input type="submit">
            </form> 
        </div>
        <?php
    }

    function isAddMoviePost($post) {
        if (isset($_POST['title']) && isset($_POST['genres']))
            return true;
        return false;
    }

    function isEditMoviePost($post) {
        if (isset($_POST['id']) && isAddMoviePost($post))
            return true;
        return false;
    }

    function validateMovieForm($post) {
        $errors = Array();
        return $errors;
    }
?>
<?php
    require_once "functions.php";
    function getRatingForm($movieId = -1) {
        $userId = 0;
        $rating = 0.5;
        include("header.php");
        ?>
        <div class="col-8">
            <form action=<?php echo "rating_add.php" ?> method="post">
                <div class="mb-3">
                    <label for="userId" class="form-label">userId</label>
                    <input type="text" class="form-control" name="userId" id="userId" value="<?php echo $userId?>">
                </div>
                <div class="mb-3">
                    <label for="movieId" class="form-label">movieId</label>
                    <input type="text" class="form-control" name="movieId" id="movieId" value="<?php echo $movieId?>">
                </div>
                <div class="mb-3">
                    <label for="rating" class="form-label">rating</label>
                    <input type="text" class="form-control" name="rating" id="rating" value="<?php echo $rating?>">
                </div>
                <input type="submit">
            </form> 
        </div>
        <?php
    }

    function isAddRatingPost($post) {
        if (isset($_POST['userId']) &&
            isset($_POST['movieId']) &&
            isset($_POST['rating']))
            return true;
        return false;
    }

    function validateRatingForm($post) {
        $errors = Array();
        return $errors;
    }
?>
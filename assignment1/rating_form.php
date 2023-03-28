<?php
    require_once "functions.php";
    function getRatingForm($userId, $movieId) {
        $update = false;
        $rating = '';
        $timestamp = '';
        if ($update) {
            
        }
        include("header.php");
        ?>
        <div class="col-8">
            <form action=<?php ($update) ? (print "rating_edit.php") : (print "rating_add.php"); ?> method="post">
                <?php
                    if (!$userId) {
                        ?>
                            <div class="mb-3">
                                <label for="userId" class="form-label">User ID</label>
                                <input type="number" step="1" class="form-control" name="userId" id="userId" value="<?php echo $userId?>">
                            </div>
                        <?php
                    }
                    else {
                        ?>
                            <input name="userId" id="userId" value=<?php echo $userId?> type="hidden">
                        <?php
                    }

                    if (!$movieId) {
                        ?>
                            <div class="mb-3">
                                <label for="movieId" class="form-label">Movie ID</label>
                                <input type="number" step="1" class="form-control" name="movieId" id="movieId" value="<?php echo $movieId?>">
                            </div>
                        <?php
                    }
                    else {
                        ?>
                            <input name="movieId" id="movieId" value=<?php echo $movieId?> type="hidden">
                        <?php
                    }
                ?>
                <div class="mb-3">
                    <label for="rating" class="form-label">Rating</label>
                    <input type="number" step="0.1" min="0.0" max="1.0" class="form-control" name="rating" id="rating" value="<?php echo $rating?>">
                </div>
                <input type="submit">
            </form> 
        </div>
        <?php
    }

    function isAddRatingPost($post) {
        if (isset($_POST['userId']) && isset($_POST['movieId']) && isset($_POST['rating']))
            return true;
        return false;
    }

    function isEditRatingPost($post) {
        return false;
    }

    function validateRatingForm($post) {
        $errors = Array();
        return $errors;
    }
?>
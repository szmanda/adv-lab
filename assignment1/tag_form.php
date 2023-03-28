<?php
    require_once "functions.php";
    function getTagForm($movieId = -1) {
        $userId = "";
        $tag = "";
        include("header.php");
        ?>
        <div class="col-8">
            <form action=<?php echo "tag_add.php" ?> method="post">
                <div class="mb-3">
                    <label for="userId" class="form-label">userId</label>
                    <input type="text" class="form-control" name="userId" id="userId" value="<?php echo $userId?>">
                </div>
                <div class="mb-3">
                    <label for="movieId" class="form-label">movieId</label>
                    <input type="text" class="form-control" name="movieId" id="movieId" value="<?php echo $movieId?>">
                </div>
                <div class="mb-3">
                    <label for="tag" class="form-label">tag</label>
                    <input type="text" class="form-control" name="tag" id="tag" value="<?php echo $tag?>">
                </div>
                <input type="submit">
            </form> 
        </div>
        <?php
    }

    function isAddTagPost($post) {
        if (isset($_POST['userId']) &&
            isset($_POST['movieId']) &&
            isset($_POST['tag']))
            return true;
        return false;
    }

    function validateTagForm($post) {
        $errors = Array();
        return $errors;
    }
?>
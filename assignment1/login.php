<?php
session_start();
include("header.php");

// if the form is submitted, add the userId to the session
if (isset($_POST['userId'])) {
    $_SESSION['userId'] = $_POST['userId'];
    header("Location: index.php");
}
// display a form fo add userId to the session
else {
    ?>
        <form action="login.php" method="post">
            <div class="mb-3">
                <label for="userId" class="form-label">User ID</label>
                <input type="number" step="1" class="form-control" name="userId" id="userId">
            </div>
            <input type="submit">
        </form>
    <?php
}
?>
<?php include("header.php") ?>

<h1>Ratings</h1>
<!-- RATINGS -->
<!-- Buttons for handling pagination -->
<?php
    $page = 0;
    if (isset($_GET['page']))
        $page = $_GET['page'];
?>
<div class="d-flex justify-content-left">
    <a href="?page=0" class="btn btn-outline-secondary m-3">First</a>
    <?php if ($page > 0) { ?>
        <a href="?page=<?php echo $page - 1 ?>" class="btn btn-outline-secondary m-3">Previous</a>
    <?php }?>
    <a href="?page=<?php echo $page + 1 ?>" class="btn btn-outline-secondary m-3">Next</a>
</div>
<div class="d-flex flex-wrap">
<?php
    require_once('functions.php');
    $pageCount = 50;
    $ratings = getRatings($page * $pageCount, $pageCount);
    foreach ($ratings as $rating) {
        ?>
            <div class="card m-3">
                <div class="card-header">
                    <h4 class="card-title">
                        <?php echo $rating["rating"] ?>
                    </h4>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        <?php echo $rating["userId"] ?>
                    </p>
                    <p class="card-text">
                        <?php echo $rating["movieId"] ?>
                    </p>
                    <p class="card-text">
                        <?php echo $rating["timestamp"] ?>
                    </p>
                </div>
                <div class="card-footer text-muted">
                    
                </div>
            </div>
        <?php
    }
?>
</div>

<?php include("footer.php") ?>

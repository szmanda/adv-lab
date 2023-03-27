<h1>Ratings</h1>
<!-- RATINGS -->
<div class="d-flex flex-wrap">
<?php
    require_once('functions.php');
    $ratings = getRatings(0, 50);
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
<h1>Tags</h1>
<!-- TAGS -->
<div class="d-flex flex-wrap">
<?php
    require_once('functions.php');
    $tags = getTags(0, 50);
    foreach ($tags as $tag) {
        ?>
            <div class="card m-3">
                <div class="card-header">
                    <h4 class="card-title">
                        <?php echo $tag["tag"] ?>
                    </h4>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        <?php echo $tag["userId"] ?>
                    </p>
                    <p class="card-text">
                        <?php echo $tag["movieId"] ?>
                    </p>
                    <p class="card-text">
                        <?php echo $tag["timestamp"] ?>
                    </p>
                </div>
                <div class="card-footer text-muted">
                    
                </div>
            </div>
        <?php
    }
?>
</div>
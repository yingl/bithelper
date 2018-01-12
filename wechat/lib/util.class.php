<?php

class Util {
    private $dao;

    public function __construct($dao) {
        $this->dao = $dao;
    }

    public function fetch_code($code) {
        $query = 'select * from btc_values where code = ? order by updated_at desc limit 1';
        $info = $this->dao->execute_with_fetch($query, array($code));
        $price = $info[0]['price'];
        $updated_at = $info[0]['updated_at'];
        return ['price' => $price, 'updated_at' => $updated_at];
    }
}

?>

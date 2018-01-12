<?php

error_reporting(E_ERROR | E_WARNING | E_PARSE);

include 'config.php';

$type = $wechat->getRev()->getRevType();
$openid = $wechat->getRevFrom();

switch($type) {
    case Wechat::MSGTYPE_TEXT: // Current use text to query coin info directly
        $code = $wechat->getRevContent();
        if (in_array($code, $coins)) {
            $data = $util->fetch_code($code);
            $text = $code . ': ' . $data['price'] . ",\n";
            $text .= '更新时间' . $data['updated_at'] . '。';
            $wechat->text($text)->reply();
        }
        else {
            $wechat->text('无法找到' . $code . '对应的币种')->reply();
        }
    case Wechat::MSGTYPE_EVENT:
        $event_array = $wechat->getRevEvent();
        $event_type = $event_array['event'];
        if ($event_type == 'subscribe') {
            $text = '欢迎访问比特小助手，数据来源OKEX，' . "\n";
            $text .= '数据刷新时间大约15~30秒。';
            $wechat->text($text)->reply();
        }
        else if ($event_type = 'CLICK') {
            if ($event_key == 'btc_top_10') {
                // TODO: BTC TOP 10
            }
            else if ($event_key == 'btc_bottom_10') {
                // TODO: BTC BOTTOM 10
            }
            else if ($event_key == 'cash') {
                // TODO: cash
            }
        }
}

?>

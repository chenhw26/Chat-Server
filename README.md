# 游戏协议

## 客户端向服务器发送的请求：

发起游戏请求: `'50' + 对方id`

## 若对方不在线：

服务器向客户端发送：`'52' + 对方id + 对方name`

## 若在线：

服务器向对方客户端发送：`'50' + 请求人id + 请求人name`

## 被请求客户端向服务器发送：

    1. 同意：`'51' + 请求人id`
    2. 拒绝：`'52' + 请求人id`

## 服务器向请求人客户端发送：

    1. 被请求人同意：`'51' + 被请求人id + 被请求人name`
    2. 被请求人拒绝：`'52' + 被请求人id + 被请求人name`   

## 以上id长度都为5Bytes
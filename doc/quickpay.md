## Bixin 钱包快捷支付接入指南

### 注册Vendor

第三方应用需要注册Vendor角色来收取授权、转账等用户通知。

### 申请绑定用户授权

第三方应用需要获取用户的授权才可以获取到用户的账户信息，账户信息会通过Event消息推送到Vendor注册的回调函数中，第三方应用开发商需要进行自有用户账号和币信用户账号的映射关系，用于后续给用户发币。

### 支付流程：币信钱包用户转账到目的账户

### 收款流程：其他账户转账到币信钱包用户

### 退款流程：其他账户退款到币信钱包用户

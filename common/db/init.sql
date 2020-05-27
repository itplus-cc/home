
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限名称',
  `url` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'url别名',
  `type` smallint(6) NOT NULL COMMENT '权限类型',
  `method` smallint(6) NOT NULL COMMENT '请求方法method',
  `isEndpoint` tinyint(1) NOT NULL COMMENT 'url是否是endpoint 否则是 url',
  `pid` int(11) NOT NULL COMMENT '上级权限',
  `isPublic` tinyint(1) NOT NULL COMMENT '是否公共权限',



INSERT INTO `auth` VALUES (1,'2019-04-24 15:39:36','2019-04-24 15:39:36','首页','system.index',1,1,1,0,1);
INSERT INTO `auth` VALUES (2,'2019-04-24 15:40:03','2019-04-25 14:51:33','系统设置','system',0,0,1,0,1);
INSERT INTO `auth` VALUES (3,'2019-04-24 15:40:20','2019-04-24 15:40:20','用户管理','systam.user',1,1,1,2,1);
INSERT INTO `auth` VALUES (4,'2019-04-24 18:55:11','2019-04-24 18:55:11','菜单管理','system.menu',1,1,1,2,1);
INSERT INTO `auth` VALUES (5,'2019-04-24 18:55:29','2019-04-26 11:18:38','权限管理','system.auth',1,1,1,2,0);
INSERT INTO `auth` VALUES (6,'2019-04-26 11:16:59','2019-04-26 11:16:59','角色管理','system.role',1,1,1,2,0);


INSERT INTO `menu` VALUES (1,'2019-04-24 20:06:38','2019-04-24 20:06:38','system','Main','系统设置','ios-cube',0,0,2,0,0);
INSERT INTO `menu` VALUES (2,'2019-04-24 20:07:57','2019-04-24 20:07:57','menu','system/menu/menu.vue','菜单管理','md-person',0,0,4,0,1);
INSERT INTO `menu` VALUES (3,'2019-04-24 20:08:20','2019-04-24 20:08:31','auth','system/auth/auth.vue','权限管理','md-person',0,0,5,0,1);
INSERT INTO `menu` VALUES (4,'2019-04-26 13:55:09','2019-04-26 14:04:45','role','system/role/role.vue','角色管理','md-radio-button-off',0,0,6,0,1);
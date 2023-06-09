-- assignment1.work_orders definition

CREATE TABLE `work_orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `work_order_number` varchar(50) DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `assigned_to` varchar(50) DEFAULT NULL,
  `room` varchar(50) DEFAULT NULL,
  `started_at` datetime DEFAULT NULL,
  `finished_at` datetime DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `work_order_number` (`work_order_number`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

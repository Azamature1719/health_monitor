package com.azamat.health_monitor_mobile.data.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.azamat.health_monitor_mobile.data.entity.OrderEntity

@Dao
interface OrderDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOne(order: OrderEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(orders: List<OrderEntity>)

    @Query("SELECT * FROM orders WHERE orderId = :id")
    suspend fun getOneById(id: Int): OrderEntity?

    @Query("SELECT * FROM orders")
    suspend fun getAll(): List<OrderEntity>

    @Query("SELECT EXISTS (SELECT 1 FROM orders WHERE orderId = :id)")
    suspend fun exists(id: Int): Boolean

    @Query("DELETE FROM orders")
    suspend fun deleteAll()

    @Query("SELECT * FROM orders WHERE endDate < :currentDate")
    suspend fun getExpiredOrders(currentDate: String): List<OrderEntity>

    @Query("DELETE FROM orders WHERE orderId = :orderId")
    suspend fun deleteOrder(orderId: Int)
}
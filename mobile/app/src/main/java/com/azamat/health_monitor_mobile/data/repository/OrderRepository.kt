package com.azamat.health_monitor_mobile.data.repository

import com.azamat.health_monitor_mobile.data.db.OrderDao
import com.azamat.health_monitor_mobile.data.entity.OrderEntity
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class OrderRepository @Inject constructor(
    private val dao: OrderDao
){
    suspend fun insertAll(orders: List<OrderEntity>) = dao.insertAll(orders)
    suspend fun insertOne(order: OrderEntity) = dao.insertOne(order)
    suspend fun getOneById(id: Int):OrderEntity? = dao.getOneById(id)
    suspend fun getOrders(): List<OrderEntity> = dao.getAll()
    suspend fun exists(id: Int): Boolean = dao.exists(id)
    suspend fun deleteAll() = dao.deleteAll()
}
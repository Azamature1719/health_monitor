package com.azamat.health_monitor_mobile.data.api

import com.azamat.health_monitor_mobile.data.model.OrderDto
import com.azamat.health_monitor_mobile.data.model.ResultDto
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {
    @GET("orders/")
    suspend fun getOrders(): List<OrderDto>

    @POST("results/")
    suspend fun sendResult(@Body result: ResultDto)
}

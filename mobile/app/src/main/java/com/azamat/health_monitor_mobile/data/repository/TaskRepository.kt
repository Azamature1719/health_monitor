@file:Suppress("UNREACHABLE_CODE")

package com.azamat.health_monitor_mobile.data.repository

import android.util.Log
import com.azamat.health_monitor_mobile.data.db.TaskDao
import com.azamat.health_monitor_mobile.data.api.ApiService
import com.azamat.health_monitor_mobile.data.db.OrderDao
import com.azamat.health_monitor_mobile.data.db.ResultDao
import com.azamat.health_monitor_mobile.data.entity.OrderEntity
import com.azamat.health_monitor_mobile.data.entity.ResultEntity
import com.azamat.health_monitor_mobile.data.entity.TaskEntity
import com.azamat.health_monitor_mobile.data.model.ResultDto
import com.azamat.health_monitor_mobile.domain.model.TaskStatus
import com.azamat.health_monitor_mobile.domain.model.getTaskTypeByString
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.withContext
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.format.DateTimeFormatter
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class TaskRepository @Inject constructor(
    private val taskDao: TaskDao,
    private val orderDao: OrderDao,
    private val resultDao: ResultDao,
    private val apiService: ApiService
) {
    suspend fun insertAllTasks(tasks: List<TaskEntity>) = taskDao.insertAll(tasks)
    suspend fun generateTasksForToday(order: OrderEntity) {
        withContext(Dispatchers.IO) {

            val formatter = DateTimeFormatter.ISO_LOCAL_DATE
            val today = LocalDate.now()
            val end = LocalDate.parse(order.endDate, formatter)

            // Условие необходимо для проверки на наличие истёкших назначений
            if(end >= today) {
                order.executionTimes.forEach { execTime ->
                    val time = LocalTime.parse(execTime)
                    val dateTime = LocalDateTime.of(today, time)

                    Log.d("TaskRepo_DateTime", "Дата и время задачи: ${dateTime.toString()}")
                    val exists = taskDao.taskExists(
                        orderId = order.orderId,
                        scheduledTime = dateTime,
                        type = order.typeName,
                        title = order.title)

                    Log.d("TaskRepo_TaskExists?: ",  exists.toString())

                    if (!exists) {
                        val task = TaskEntity(
                            orderId = order.orderId,
                            title = order.title,
                            scheduledTime = dateTime,
                            status = TaskStatus.pending,
                            type = getTaskTypeByString(order.typeName),
                            doctorId = order.doctorId,
                            doctorInfo = order.doctorInfo
                        )
                        Log.d("TaskRepo: ", "Запишется в базу: ${task}")
                        taskDao.insertOne(task)
                    }
                }
            }
            else{
                Log.d("TaskRepo_Срок_назн_истёк:",  "${order}")
            }
        }
    }

    fun getTasksForDate(date: String): Flow<List<TaskEntity>> = taskDao.getTasksForDate(date)
    suspend fun taskExists(orderId: Int, scheduledTime: LocalDateTime, type: String, title: String): Boolean = taskDao.taskExists(orderId, scheduledTime, type, title)
    suspend fun submitResult(taskId: Int, value: Float){
        val result = ResultEntity(
            taskId = taskId,
            value = value
        )
        resultDao.insert(result)

        val task = taskDao.getTaskById(taskId)
        if(task != null){
            val order = orderDao.getOneById(task.orderId)
            val resultDto = ResultDto(
                resultId = result.id,
                value = result.value,
                patientId = 1, //TODO (после реализации аут-ции брать из UserSession)
                orderId = task.orderId,
                typeName = task.type.toString(),
                title = task.title,
                unit = order!!.unit, // -- Предполагаем, что по задаче назначение всегда существует --
                executionTime = result.timestamp.toString(),
                status = task.status.name,
                doctorId = task.doctorId
            )
            try {
                Log.e("TaskRepository", "Отправлен результат: ${resultDto}")
                apiService.sendResult(resultDto)
            } catch (e: Exception){
                Log.e("TaskRepository", "Ошибка отправки результата: ${e.message}")
            }

        }
    }
    suspend fun updateTaskStatus(taskId: Int, status: TaskStatus) = taskDao.updateStatus(taskId, status)
}
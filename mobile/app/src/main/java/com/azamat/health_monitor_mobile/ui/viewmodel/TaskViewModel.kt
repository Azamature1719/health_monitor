package com.azamat.health_monitor_mobile.ui.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.azamat.health_monitor_mobile.data.api.ApiService
import com.azamat.health_monitor_mobile.data.repository.OrderRepository
import com.azamat.health_monitor_mobile.data.repository.TaskRepository
import com.azamat.health_monitor_mobile.domain.mappers.toDomain
import com.azamat.health_monitor_mobile.domain.model.TaskDomain
import com.azamat.health_monitor_mobile.domain.model.TaskStatus
import com.azamat.health_monitor_mobile.domain.model.TaskType
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.format.DateTimeFormatter
import javax.inject.Inject

@HiltViewModel
class TaskViewModel @Inject constructor(
    private val taskRepository: TaskRepository,
    private val orderRepository: OrderRepository,
    private val apiService: ApiService
) : ViewModel() {

    private val _tasks = MutableStateFlow<List<TaskDomain>>(emptyList())
    val tasks: StateFlow<List<TaskDomain>> = _tasks.asStateFlow()
    val tag: String = "TaskViewModel"

    init {
        viewModelScope.launch {
            fetchOrders()
            // generateTasks()
            // loadTodayTasks()
            loadTestTasks()
        }
    }

    val openTasks: StateFlow<List<TaskDomain>> = _tasks.map { tasks ->
        tasks.filter { it.status == TaskStatus.pending || it.status == TaskStatus.missed}
            .sortedBy { it.scheduledTime }
    }.stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    val doneTasks: StateFlow<List<TaskDomain>> = _tasks
        .map { tasks ->
            tasks.filter { it.status == TaskStatus.done }
                .sortedBy { it.scheduledTime }
        }
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun updateTasks(newTasks: List<TaskDomain>) {
        _tasks.value = newTasks
    }

    private suspend fun fetchOrders() {
        try {
            val orders = apiService.getOrders()
            val orderEntities = orders.map { it.toEntity() }
            Log.d("TaskVM_FetchOrders", "Назначения получены: $orderEntities")

            val formatter = DateTimeFormatter.ISO_LOCAL_DATE
            val today = LocalDate.now().toString()

            orderEntities.forEach{
                orderEntity ->
                if(orderEntity.endDate > today){
                    if(!orderRepository.exists(orderEntity.orderId)){
                        orderRepository.insertOne(orderEntity)
                        Log.d("TaskVM_FetchOrders", "Записан в базу: ${orderEntity}")
                    }
                    else{
                        Log.d("TaskVM_FetchOrders", "Назначение существует ${orderEntity}")
                    }
                }
                else{
                    Log.d("TaskVM_FetchOrders", "Назначение истекло ${orderEntity}")
                }
            }
        } catch (e: Exception) {
            Log.e("TaskVM_FetchOrders", "Ошибка получения: ${e.message}")
        }
    }

    private suspend fun generateTasks(){
        try {
            val ordersEntities = orderRepository.getOrders()
            Log.d("TaskVM_GenerateTasks", "Взяты из БД:$ordersEntities")

            ordersEntities.forEach{ orderEntity ->
                taskRepository.generateTasksForToday(orderEntity)
            }
        }
        catch (e: Exception){
            Log.d("TaskVM_GenerateTasks", e.message.toString())
        }
    }

    private suspend fun loadTodayTasks() {
        try {
            taskRepository.getTasksForDate(LocalDate.now().toString())
                .map { list -> list.map{it.toDomain()} }
                .collect{ domainTasks -> _tasks.value = domainTasks
                Log.d("TaskVM_DomainTasks", domainTasks.toString())}
        }
        catch (e: Exception){
            Log.d("TaskVM_LoadTodayTasks", e.message.toString())
        }

    }

    private fun loadTestTasks() {
        viewModelScope.launch {
            // 🔽 Временные тестовые задачи
            val testTasks = listOf(
                TaskDomain(
                    id = 1,
                    orderId = 1,
                    title = "Измерить температуру",
                    scheduledTime = LocalDateTime.of(LocalDate.now(), LocalTime.of(20, 0)),
                    status = TaskStatus.pending,
                    doctorInfo = "Невролог",
                    type = TaskType.temperature
                ),
                TaskDomain(
                    id = 2,
                    orderId = 1,
                    title = "Измерить давление",
                    scheduledTime = LocalDateTime.of(LocalDate.now(), LocalTime.of(21, 0)),
                    status = TaskStatus.pending,
                    doctorInfo = "Невролог",
                    type = TaskType.pressure
                ),
                TaskDomain(
                    id = 3,
                    orderId = 1,
                    title = "Оценить уровень настроения",
                    scheduledTime = LocalDateTime.of(LocalDate.now(), LocalTime.of(16, 0)),
                    status = TaskStatus.pending,
                    doctorInfo = "Терапевт",
                    type = TaskType.mood
                ),
                TaskDomain(
                    id = 4,
                    orderId = 4,
                    title = "Измерить сердцебиение",
                    scheduledTime = LocalDateTime.of(LocalDate.now(), LocalTime.of(12, 0)),
                    status = TaskStatus.done,
                    doctorInfo = "Кардиолог",
                    type = TaskType.heart_rate
                ),
                TaskDomain(
                    id = 4,
                    orderId = 4,
                    title = "Измерить давление",
                    scheduledTime = LocalDateTime.of(LocalDate.now(), LocalTime.of(14, 0)),
                    status = TaskStatus.done,
                    doctorInfo = "Кардиолог",
                    type = TaskType.pressure
                ),
                TaskDomain(
                    id = 4,
                    orderId = 4,
                    title = "Измерить сатурацию",
                    scheduledTime = LocalDateTime.of(LocalDate.now(), LocalTime.of(10, 0)),
                    status = TaskStatus.missed,
                    doctorInfo = "Кардиолог",
                    type = TaskType.saturation
                ),
                TaskDomain(
                    id = 4,
                    orderId = 4,
                    title = "Измерить настроение",
                    scheduledTime = LocalDateTime.of(LocalDate.now(), LocalTime.of(17, 0)),
                    status = TaskStatus.missed,
                    doctorInfo = "Кардиолог",
                    type = TaskType.mood
                )
            )
            _tasks.value = testTasks
        }
    }


}

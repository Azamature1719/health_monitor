package com.azamat.health_monitor_mobile.ui.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.azamat.health_monitor_mobile.data.api.ApiService
import com.azamat.health_monitor_mobile.data.repository.TaskRepository
import com.azamat.health_monitor_mobile.domain.model.TaskStatus
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject


@HiltViewModel
class ManualInputViewModel @Inject constructor(
    private val apiService: ApiService,
    private val taskRepository: TaskRepository
): ViewModel() {

    fun submitResult(taskId: Int, inputValue: Float){
         viewModelScope.launch {
             try {
                 taskRepository.submitResult(taskId, inputValue)
                 // TODO(Для WorkManager'a изменить, так как он будет проставлять статус в зависимости от usecase'a)
                 taskRepository.updateTaskStatus(taskId, TaskStatus.done)
             }
             catch (e: Exception) {
                 Log.d("ManualInput_VM", e.message.toString())
             }
         }
    }
}

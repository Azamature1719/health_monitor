package com.azamat.health_monitor_mobile.ui.viewmodel

import android.util.Log
import android.widget.Toast
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import com.azamat.health_monitor_mobile.data.api.ApiService
import com.azamat.health_monitor_mobile.data.repository.OrderRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class OrderViewModel @Inject constructor(
    private val repository: OrderRepository,
    private val apiService: ApiService
) : ViewModel() {
    init {
    }
}

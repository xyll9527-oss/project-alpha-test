<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="modal-overlay" @click.self="close">
        <div class="modal-container">
          <!-- 头部 -->
          <div class="modal-header">
            <h2 class="modal-title">{{ isEdit ? '编辑 Ticket' : '新建 Ticket' }}</h2>
            <button class="close-btn" @click="close">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M18 6L6 18M6 6l12 12" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- 表单内容 -->
          <div class="modal-body">
            <form @submit.prevent="handleSubmit" class="form">
              <!-- 名称 -->
              <div class="form-group">
                <label class="form-label">
                  名称
                  <span class="required">*</span>
                </label>
                <input
                  v-model="form.name"
                  type="text"
                  class="form-input"
                  placeholder="输入 Ticket 名称"
                  required
                />
              </div>

              <!-- 描述 -->
              <div class="form-group">
                <label class="form-label">描述</label>
                <textarea
                  v-model="form.description"
                  class="form-textarea"
                  placeholder="添加详细描述（可选）"
                  rows="4"
                />
              </div>



              <!-- 标签 -->
              <div class="form-group">
                <label class="form-label">标签</label>
                <div v-if="tags.length > 0" class="tag-options">
                  <label
                    v-for="tag in tags"
                    :key="tag.id"
                    class="tag-option"
                    :class="{ selected: form.tag_ids.includes(tag.id) }"
                    :style="getTagStyle(tag)"
                  >
                    <input
                      v-model="form.tag_ids"
                      type="checkbox"
                      :value="tag.id"
                      class="tag-checkbox"
                    />
                    <span class="tag-name">{{ tag.name }}</span>
                  </label>
                </div>
                <p v-else class="empty-tags">暂无标签，请先创建标签</p>
              </div>
            </form>
          </div>

          <!-- 底部操作 -->
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="close">取消</button>
            <button 
              class="btn btn-primary" 
              :disabled="!form.name.trim() || submitting"
              @click="handleSubmit"
            >
              {{ submitting ? '保存中...' : (isEdit ? '保存' : '创建') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, reactive, computed } from 'vue';
import type { Ticket, Tag, TicketCreate, TicketUpdate } from '@/types';
import { useApi } from '@/composables/useApi';

const props = defineProps<{
  visible: boolean;
  ticket: Ticket | null;
  tags: Tag[];
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit'): void;
}>();

const api = useApi();

const isEdit = ref(false);
const submitting = ref(false);

const statusOptions = [
  { label: '待办', value: 'pending' },
  { label: '已完成', value: 'completed' }
];

const form = reactive({
  name: '',
  description: '',
  status: 'pending' as 'pending' | 'completed',
  tag_ids: [] as number[]
});

/**
 * 获取标签样式
 */
const getTagStyle = (tag: Tag) => {
  const isSelected = form.tag_ids.includes(tag.id);
  return {
    backgroundColor: isSelected ? tag.color : tag.color + '15',
    color: isSelected ? '#fff' : tag.color,
    borderColor: tag.color + '40'
  };
};

/**
 * 关闭弹窗
 */
const close = () => {
  emit('close');
};

/**
 * 提交表单
 */
const handleSubmit = async () => {
  if (!form.name.trim() || submitting.value) return;

  submitting.value = true;
  try {
    if (isEdit.value && props.ticket) {
      const updateData: TicketUpdate = {
        name: form.name,
        description: form.description || undefined,
        status: form.status
      };
      await api.updateTicket(props.ticket.id, updateData);
      
      // 更新标签关联
      const currentTagIds = props.ticket.tags.map(t => t.id);
      const addedTags = form.tag_ids.filter(id => !currentTagIds.includes(id));
      const removedTags = currentTagIds.filter(id => !form.tag_ids.includes(id));

      for (const tagId of addedTags) {
        await api.addTagToTicket(props.ticket.id, tagId);
      }
      for (const tagId of removedTags) {
        await api.removeTagFromTicket(props.ticket.id, tagId);
      }
    } else {
      const createData: TicketCreate = {
        name: form.name,
        description: form.description || undefined,
        status: form.status,
        tag_ids: form.tag_ids.length > 0 ? form.tag_ids : undefined
      };
      await api.createTicket(createData);
    }

    emit('submit');
  } catch (error) {
    console.error('提交失败:', error);
    alert(isEdit.value ? '保存失败' : '创建失败');
  } finally {
    submitting.value = false;
  }
};

/**
 * 监听visible变化，初始化表单
 */
watch(() => props.visible, (val) => {
  if (val) {
    if (props.ticket) {
      isEdit.value = true;
      form.name = props.ticket.name;
      form.description = props.ticket.description || '';
      form.status = props.ticket.status;
      form.tag_ids = props.ticket.tags.map(t => t.id);
    } else {
      isEdit.value = false;
      form.name = '';
      form.description = '';
      form.status = 'pending';
      form.tag_ids = [];
    }
  }
});
</script>

<style scoped>
/* 遮罩层 */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  padding: 20px;
}

/* 弹窗容器 */
.modal-container {
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  background: var(--color-canvas);
  border-radius: var(--radius-lg);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 头部 */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-divider);
}

.modal-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: var(--color-ink);
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.close-btn:hover {
  background: var(--color-canvas-parchment);
}

.close-btn svg {
  width: 20px;
  height: 20px;
  color: var(--color-body-muted);
}

/* 内容区 */
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

/* 表单 */
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-ink);
}

.required {
  color: #ff3b30;
  margin-left: 2px;
}

.form-input,
.form-textarea {
  padding: 12px 16px;
  font-size: 16px;
  font-family: var(--font-text);
  color: var(--color-body);
  background: var(--color-canvas);
  border: 1px solid var(--color-hairline);
  border-radius: var(--radius-md);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: var(--color-body-muted);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

/* 状态选项 */
.status-options {
  display: flex;
  gap: 12px;
}

.status-option {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: var(--color-canvas-parchment);
  border: 2px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.status-option:hover {
  background: var(--color-surface-pearl);
}

.status-option.active {
  border-color: var(--color-primary);
  background: rgba(0, 102, 204, 0.05);
}

.status-radio {
  display: none;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-dot.pending {
  background: #ff9500;
}

.status-dot.completed {
  background: #34c759;
}

.status-label {
  font-size: 15px;
  color: var(--color-body);
}

/* 标签选项 */
.tag-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-option {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 9999px;
  border: 1px solid;
  cursor: pointer;
  transition: all 0.2s;
}

.tag-option:hover {
  opacity: 0.8;
}

.tag-checkbox {
  display: none;
}

.tag-name {
  font-size: 13px;
  font-weight: 500;
}

.empty-tags {
  font-size: 14px;
  color: var(--color-body-muted);
  padding: 12px;
  background: var(--color-canvas-parchment);
  border-radius: var(--radius-md);
  text-align: center;
}

/* 底部 */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--color-divider);
  background: var(--color-surface-pearl);
}

.btn {
  padding: 11px 22px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  color: var(--color-body);
  background: transparent;
}

.btn-secondary:hover {
  background: var(--color-canvas-parchment);
}

.btn-primary {
  color: white;
  background: var(--color-primary);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-focus);
}

/* 动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
  opacity: 0;
}

/* 响应式 */
@media (max-width: 640px) {
  .modal-overlay {
    padding: 0;
    align-items: flex-end;
  }

  .modal-container {
    max-height: 85vh;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  }

  .modal-header {
    padding: 16px 20px;
  }

  .modal-body {
    padding: 20px;
  }

  .modal-footer {
    padding: 12px 20px;
  }

  .status-options {
    flex-direction: column;
  }
}
</style>

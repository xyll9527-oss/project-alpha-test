<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="modal-overlay" @click.self="close">
        <div class="modal-container">
          <!-- 头部 -->
          <div class="modal-header">
            <h2 class="modal-title">标签管理</h2>
            <button class="close-btn" @click="close">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M18 6L6 18M6 6l12 12" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- 内容区 -->
          <div class="modal-body">
            <!-- 添加标签表单 -->
            <div class="add-tag-section">
              <h3 class="section-subtitle">添加新标签</h3>
              <div class="add-tag-form">
                <input
                  v-model="newTag.name"
                  type="text"
                  class="form-input"
                  placeholder="标签名称"
                  @keyup.enter="handleCreateTag"
                />
                <div class="color-picker-wrapper">
                  <input
                    v-model="newTag.color"
                    type="color"
                    class="color-picker"
                  />
                  <span class="color-value">{{ newTag.color }}</span>
                </div>
                <button 
                  class="btn btn-primary" 
                  :disabled="!newTag.name.trim()"
                  @click="handleCreateTag"
                >
                  添加
                </button>
              </div>
            </div>

            <!-- 标签列表 -->
            <div class="tags-list-section">
              <h3 class="section-subtitle">
                现有标签
                <span class="tag-count">{{ tags.length }}</span>
              </h3>
              
              <div v-if="tags.length === 0" class="empty-state">
                <p>暂无标签</p>
              </div>
              
              <div v-else class="tags-grid">
                <div
                  v-for="tag in tags"
                  :key="tag.id"
                  class="tag-item"
                >
                  <div class="tag-preview" :style="{ backgroundColor: tag.color }">
                    <span class="tag-preview-name">{{ tag.name }}</span>
                  </div>
                  <div class="tag-info">
                    <span class="tag-name">{{ tag.name }}</span>
                    <span class="tag-color">{{ tag.color }}</span>
                  </div>
                  <button 
                    class="delete-btn" 
                    @click="handleDeleteTag(tag.id)"
                    title="删除标签"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import type { Tag, TagCreate } from '@/types';
import { useApi } from '@/composables/useApi';

const props = defineProps<{
  visible: boolean;
  tags: Tag[];
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'update'): void;
}>();

const api = useApi();

const newTag = reactive<TagCreate>({
  name: '',
  color: '#0066cc'
});

/**
 * 关闭弹窗
 */
const close = () => {
  emit('close');
  // 重置表单
  newTag.name = '';
  newTag.color = '#0066cc';
};

/**
 * 创建标签
 */
const handleCreateTag = async () => {
  if (!newTag.name.trim()) return;

  try {
    await api.createTag(newTag);
    newTag.name = '';
    newTag.color = '#0066cc';
    emit('update');
  } catch (error) {
    console.error('创建标签失败:', error);
    alert('创建标签失败');
  }
};

/**
 * 删除标签
 */
const handleDeleteTag = async (id: number) => {
  if (!confirm('确定要删除这个标签吗？相关的 Ticket 将不再显示此标签。')) return;

  try {
    await api.deleteTag(id);
    emit('update');
  } catch (error) {
    console.error('删除标签失败:', error);
    alert('删除标签失败');
  }
};
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
  max-width: 560px;
  max-height: 80vh;
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

.section-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-ink);
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tag-count {
  font-size: 13px;
  font-weight: 400;
  color: var(--color-body-muted);
  background: var(--color-canvas-parchment);
  padding: 2px 8px;
  border-radius: 9999px;
}

/* 添加标签 */
.add-tag-section {
  margin-bottom: 32px;
}

.add-tag-form {
  display: flex;
  gap: 12px;
  align-items: center;
}

.form-input {
  flex: 1;
  padding: 10px 14px;
  font-size: 15px;
  font-family: var(--font-text);
  color: var(--color-body);
  background: var(--color-canvas);
  border: 1px solid var(--color-hairline);
  border-radius: var(--radius-md);
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: var(--color-primary);
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  background: var(--color-canvas-parchment);
  border-radius: var(--radius-md);
}

.color-picker {
  width: 32px;
  height: 32px;
  padding: 0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background: none;
}

.color-value {
  font-size: 13px;
  font-family: monospace;
  color: var(--color-body-muted);
}

.btn {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  color: white;
  background: var(--color-primary);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-focus);
}

/* 标签列表 */
.tags-list-section {
  border-top: 1px solid var(--color-divider);
  padding-top: 24px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--color-body-muted);
  font-size: 15px;
}

.tags-grid {
  display: grid;
  gap: 12px;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--color-canvas-parchment);
  border-radius: var(--radius-md);
  transition: background 0.2s;
}

.tag-item:hover {
  background: var(--color-surface-pearl);
}

.tag-preview {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tag-preview-name {
  font-size: 11px;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  max-width: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tag-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.tag-name {
  font-size: 15px;
  font-weight: 500;
  color: var(--color-ink);
}

.tag-color {
  font-size: 13px;
  font-family: monospace;
  color: var(--color-body-muted);
}

.delete-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  opacity: 0;
}

.tag-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background: rgba(255, 59, 48, 0.1);
}

.delete-btn svg {
  width: 18px;
  height: 18px;
  color: var(--color-body-muted);
}

.delete-btn:hover svg {
  color: #ff3b30;
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

  .add-tag-form {
    flex-direction: column;
    align-items: stretch;
  }

  .color-picker-wrapper {
    justify-content: space-between;
  }

  .delete-btn {
    opacity: 1;
  }
}
</style>
